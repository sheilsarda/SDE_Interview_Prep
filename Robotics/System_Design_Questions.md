# Robotics System Design — Interview Question Bank

> **Format:** Whiteboard-style system design interview
> **Time per question:** ~45-60 minutes
> **Level:** Senior / Staff Robotics Software Engineer
> **Focus:** Distributed Systems, Data Pipelines, Algorithmic Robotics, and ML

---

## Question 1: Distributed Fleet Telemetry and Log Ingestion System

### Problem

You are tasked with designing a system that manages a global fleet of 10,000 quadruped inspection robots. These robots operate in disparate environments with highly intermittent cellular connectivity. The system needs to ingest live telemetry for dashboards, and upload heavy ROS logs for persistent storage and debugging.

**Part A (Edge Agent & Data Uploader, ~15 min)**
The quadruped controller produces high-frequency joint states and low-frequency system diagnostics via ROS 2. Design the edge agent responsible for the "Data Uploader." How do you handle intermittent internet without losing data? How do you prioritize live telemetry over massive log files?

**Part B (Log Compression, ~15 min)**
Discuss compression strategies for robotics logs. How do you compress high-bandwidth topics like images or dense point clouds before uploading? What are the tradeoffs between lossless and lossy compression on edge hardware?

**Part C (Backend & Caching, ~20 min)**
Design the backend ingestion service. The central dashboard requires ultra-low latency access to the last known state (pose, battery, current task) of any robot. Explain how you would manage hot state data in this design.

---

### A+ Response Benchmark

#### Part A — Edge Agent & Data Uploader

- **Process Isolation (Not Just "Separate Node"):** The Edge Agent must run as its own **OS process** with its own ROS 2 executor, separate from the real-time control loop. The isolation mechanism is critical: a naive implementation that places the agent in the same process as the controller (sharing a `MultiThreadedExecutor`) will cause any blocking I/O in the agent (disk writes, TCP connections) to introduce jitter into the control loop. The production-correct approach uses Fast DDS shared memory transport for zero-copy IPC between the controller process and the agent process on the same host — no serialization overhead, no network stack involvement.

    > *Ref: ROS 2 Executor architecture — https://docs.ros.org/en/humble/Concepts/About-Executors.html*
    > *Ref: Fast DDS shared memory transport — https://fast-dds.docs.eprosima.com/en/latest/fastdds/transport/shared_memory/shared_memory.html*

- **QoS Profile Matching:** One of the most common silent bugs in ROS 2 logging pipelines is a QoS mismatch. If the controller publishes joint states with `BEST_EFFORT` reliability (correct for high-frequency data where you don't want blocking writes), and the Edge Agent subscribes with `RELIABLE`, the DDS middleware will **silently fail the subscription** — zero messages received, no error logged. The candidate must demonstrate awareness that QoS negotiation is a real production concern and that the agent must match or be more lenient than the publisher's profile:
    - High-frequency joint states: subscribe `BEST_EFFORT`, `KEEP_LAST(1)` — only the latest state matters.
    - Low-frequency diagnostics: subscribe `RELIABLE`, `KEEP_ALL` — every message must be persisted.
    - Use `ros2 topic info --verbose` to inspect live QoS negotiation during development.

    > *Ref: ROS 2 QoS compatibility rules — https://docs.ros.org/en/humble/Concepts/About-Quality-of-Service-Settings.html*

- **Two-Tier Disk-Backed Queue with Explicit Eviction:** Implement a local disk-backed queue (e.g., SQLite in WAL mode for reliability, or RocksDB for higher throughput). The queue is split into two priority tiers:
    - **High-priority:** Telemetry heartbeats, battery alerts, E-Stop events, safety-critical diagnostics.
    - **Low-priority:** Raw image frames, point clouds, dense joint-state logs.

    A hard disk budget (e.g., 8 GB) triggers eviction of the oldest low-priority rows first. High-priority data is never evicted. This is a two-tier LRU on disk. When connectivity resumes, the uploader drains high-priority first (small, ACKed chunks), then low-priority in background threads using multipart uploads.

    > *Ref: SQLite WAL mode for concurrent read/write — https://www.sqlite.org/wal.html*

- **Bonus Signal — Backpressure Handling:** If disk fills completely (e.g., extended offline period), the agent should dynamically drop old high-frequency debug data (image frames) but retain all low-frequency critical diagnostics. The candidate should articulate this as a configurable policy, not a hard-coded behavior.

---

#### Part B — Log Compression

- **Three Distinct Compression Layers:** A senior candidate must cleanly separate these rather than conflating them under one umbrella:

    | Layer | Mechanism | Tools | Tradeoff |
    |---|---|---|---|
    | **Serialization compression** | LZ4 or ZSTD applied to serialized message bytes at the container level | rosbag2 `--compression-mode`, MCAP native compression | Lossless; minimal CPU cost; ~2-4x reduction on most topics |
    | **Temporal decimation** | Drop messages where the signal delta since the last recorded message is below a threshold | Custom ROS 2 filter node, `topic_tools/throttle` | Lossy; simple to implement; effective for slow-changing joints. Typical thresholds: 0.001 rad for joint angles, 0.005 m for position |
    | **Video codec compression** | H.264/H.265 encoding of image streams using hardware encoders | GStreamer pipeline with NVENC on Jetson, FFmpeg, `image_transport` compressed plugin | Lossy; massive reduction (10-50x for video); requires an encode pipeline integration into ROS |

    A candidate who can reason about when to apply each layer (e.g., "serialization compression always, temporal decimation for slow-moving joints, video codec for camera topics") is demonstrating staff-level thinking.

- **MCAP Format Awareness:** As of ROS 2 Humble (2022), the default rosbag2 storage plugin is **MCAP**, replacing the SQLite3-based `.db3` format. MCAP provides native LZ4/ZSTD compression per-chunk, seekable playback without full decompression, and first-class support for mixed message schemas. A senior candidate in 2025 should reference MCAP, not the legacy `.bag` format.

    > *Ref: MCAP format specification — https://mcap.dev/spec*
    > *Ref: rosbag2 MCAP storage plugin — https://github.com/ros-tooling/rosbag2_storage_mcap*

- **Hardware-Accelerated Image Compression Pipeline:** "Use NVENC for H.264" is directionally correct, but the full pipeline must be specified:
    1. A ROS 2 node subscribes to `sensor_msgs/Image` (raw, uncompressed).
    2. Frames are passed to a GStreamer pipeline or FFmpeg subprocess configured to use NVENC.
    3. The encoded stream (H.264/H.265) is either republished as `sensor_msgs/CompressedImage` or written directly to a container file for later upload.
    4. A simpler alternative is the `image_transport` package's `compressed` plugin (JPEG/PNG per-frame), which is CPU-only and less efficient but trivial to configure.

    > *Ref: ROS 2 `image_transport` — https://github.com/ros-perception/image_transport_tutorials*
    > *Ref: GStreamer NVENC plugin — https://gstreamer.freedesktop.org/documentation/nvcodec/*

- **Safety-Critical Retention Policy:** For any robot operating near humans or in a safety-critical context, raw (uncompressed) sensor data for a configurable window preceding any E-Stop or fault event (e.g., 30 seconds) must be retained uncompressed, even if the rest of the log is decimated. This is a non-negotiable requirement for safety investigation and regulatory compliance.

---

#### Part C — Backend & Hot State Management

- **Event Streaming Ingestion:** Telemetry is pushed into an Apache Kafka cluster partitioned by `robot_id`. This ensures all messages from a given robot land on the same partition, preserving ordering. A **Kafka Consumer Group** with multiple consumer instances (scaled to match partition count) reads messages in parallel.

    > *Ref: Kafka Consumer Groups — https://kafka.apache.org/documentation/#intro_consumers*

- **Hot State Layer — Redis with TTL (Not LRU Eviction):** Each consumer writes the latest robot state to Redis using pipelined commands:
    ```
    SET robot:{id}:state <serialized_proto> EX 60
    ```
    The 60-second TTL auto-expires state keys for offline robots. This is cleaner and more predictable than relying on Redis LRU eviction as a staleness mechanism.

    **Why not LRU eviction for staleness?** Redis's `maxmemory-policy allkeys-lru` evicts **entire keys**, not individual fields within a key. If you store robot state as a Redis Hash (`HSET robot:1234 pose "..." battery "..."`) and Redis needs to free memory, it evicts the entire hash for robot 1234 — losing all state, not just old data. This is a subtle production bug. Use TTL for staleness, and configure `maxmemory-policy volatile-lru` as a memory safety valve (only evicts keys that have a TTL set, if memory pressure occurs).

    > *Ref: Redis eviction policies — https://redis.io/docs/reference/eviction/*
    > *Ref: Redis pipelining — https://redis.io/docs/manual/pipelining/*

- **Cold Storage Layer:** The same Kafka consumer group (or a separate one) fans out writes to a Time-Series Database (InfluxDB, TimescaleDB, or Apache Parquet on S3 via a Flink/Spark Streaming job) for historical queries and analytics. The live dashboard reads exclusively from Redis; the analytics dashboard reads from the TSDB.

- **Dashboard Read Path:** The dashboard service reads `GET robot:{id}:state` from Redis. For the "all robots" overview, maintain a Redis Set `robots:active` that tracks robot IDs with live state keys (update on each heartbeat, remove via Set TTL or explicit `SREM` on expiry). Avoid `KEYS *` in production — it blocks the Redis event loop.

#### Architecture (UML)
![Architecture Diagram](diagram_q1.png)

---

## Question 2: Cloud-Native Kinematics and Transform (TF) Service

### Problem

You are designing a centralized motion-planning and spatial-awareness backend for a massive automated warehouse. The warehouse contains thousands of robotic arms and mobile bases. The robots need a highly scalable way to query coordinate frame data and execute matrix math dynamically.

**Part A (TF Tree System, ~10 min)**
Explain how a TF (Transform) tree system works. How would you design a system that tracks the positions of all entities in the warehouse — both for real-time robot control and for fleet-level visualization?

**Part B (Matrix Multiplication, ~15 min)**
Matrix multiplication is core to resolving coordinate frames. Explain the mathematical pipeline of getting an end-effector pose from a series of joint states. When does this computation become a scaling challenge, and when is it trivial?

**Part C (Implementing FK/IK, ~20 min)**
Design a Forward Kinematics (FK) and Inverse Kinematics (IK) microservice. If a robotic arm sends its current joint positions, how does the service compute FK? Conversely, if it sends a target pose, how do you handle IK — including failure modes?

---

### A+ Response Benchmark

#### Part A — Two-Layer Transform Architecture

- **Core Concept:** A TF tree represents spatial relationships between coordinate frames (e.g., `map → odom → base_link → camera_link`) as a Directed Acyclic Graph. Each edge carries a timestamped homogeneous transformation (4x4 matrix). In ROS 2, the `tf2` library maintains a per-frame time-indexed circular buffer and resolves transforms via tree traversal and temporal interpolation.

- **Critical Design Insight — Two Distinct Use Cases Require Two Distinct Solutions:**

    | Use Case | Frequency | Latency Requirement | Correct Solution |
    |---|---|---|---|
    | Real-time FK/transform resolution for on-robot control | 100-1000 Hz | < 1 ms | Local `tf2` buffer on the robot; never centralized |
    | Fleet-level position tracking for dashboards and coordination | 1-10 Hz | 10-100 ms acceptable | Cloud asset registry (Redis or Postgres) |

    **Why NOT a centralized graph database (e.g., Neo4j) for real-time TF:** `tf2` is fast precisely because it is a local, in-process lookup — `lookupTransform` is a hash table access plus matrix math that completes in microseconds. Centralizing this to a remote database introduces network round-trip latency (1-10 ms even on a fast LAN), making it unusable at control frequency. It also creates a single point of failure — if the DB is down, no robot can compute transforms. Additionally, 1,000 robots querying at 100 Hz = 100,000 queries/second, which is a thundering-herd pattern that most graph databases are not designed for.

    **A centralized database is only appropriate for the fleet-level use case:** Each robot's navigation stack publishes its coarse `map → base_link` localization result (a single pose) to a cloud endpoint at low frequency (1-5 Hz). This is stored in Redis (keyed by `robot_id`) for live dashboard reads, and in a TSDB for historical path visualization. This is a simple key-value store of robot poses — not a TF tree.

    For fixed warehouse infrastructure frames (conveyor positions, camera mounts, charging dock locations), publish these as `static_transform_publisher` definitions that each robot loads at startup into its local tf2 buffer.

    > *Ref: ROS 2 tf2 design — https://docs.ros.org/en/humble/Tutorials/Intermediate/Tf2/Tf2-Main.html*
    > *Ref: tf2 time-indexed buffer architecture — http://wiki.ros.org/tf2/Design*

---

#### Part B — Matrix Multiplication and Scaling

- **Mathematical Pipeline:** Each joint $i$ introduces a homogeneous transformation matrix $T_i \in SE(3)$:

    $$T_i = \begin{bmatrix} R_i & p_i \\ 0 & 1 \end{bmatrix}$$

    where $R_i \in SO(3)$ is a 3x3 rotation matrix derived from the joint angle and axis, and $p_i \in \mathbb{R}^3$ is the translation (link offset). These matrices are constructed from either **Denavit-Hartenberg (DH) parameters** (classical formulation) or directly from **URDF joint/origin definitions** (modern ROS approach, used by KDL and Pinocchio). The end-effector pose is the left-product of all joint transforms:

    $$T_{EE} = T_0 \cdot T_1 \cdot T_2 \cdots T_n$$

- **When This is Trivial (Almost Always for FK):** For a 6-DOF arm, this is 6 multiplications of 4x4 matrices. Eigen 3 (the standard C++ linear algebra library in robotics) executes this in roughly **1-5 microseconds on a single CPU core**. Even at 1 kHz control rate for 1,000 robots, a single modern multi-core server handles all FK computations with no GPU involvement. **GPU acceleration for basic FK is overkill** and indicates a misunderstanding of the compute profile.

- **When This Becomes a Scaling Challenge (Trajectory Sampling):** GPU parallelism is justified when performing **massively parallel trajectory sampling** — algorithms like Model Predictive Path Integral (MPPI) or Cross-Entropy Method (CEM) that evaluate thousands of candidate trajectories simultaneously. Each trajectory rollout requires FK at every timestep: 10,000 samples x 50 timesteps x 6 joints = 3 million matrix chain evaluations per control tick. This is where batched GPU FK (via libraries like **cuRobo**) provides genuine speedup.

    > *Ref: Eigen 3 fixed-size matrix performance — https://eigen.tuxfamily.org/*
    > *Ref: Pinocchio rigid body dynamics library — https://github.com/stack-of-tasks/pinocchio*
    > *Ref: cuRobo (NVIDIA CUDA-accelerated motion generation) — https://curobo.org/*
    > *Ref: MPPI with GPU parallelism — Williams et al., "Information-Theoretic MPC" (2017) — https://arxiv.org/abs/1707.02342*

---

#### Part C — FK/IK Microservice Design

- **FK Service (Stateless, CPU-Only):** A stateless gRPC service receives joint angles $\theta \in \mathbb{R}^n$ and a robot model identifier. It looks up the pre-loaded URDF (cached at service startup) for that model, runs the matrix chain via Pinocchio's `forwardKinematics()`, and returns the end-effector pose as $(x, y, z, q_w, q_x, q_y, q_z)$. Use quaternions, not Euler angles — Euler representations suffer from gimbal lock. FK is trivially parallelizable; horizontal scaling is straightforward with standard load balancing.

- **IK Service — Two-Tier Architecture:**

    - **Tier 1 — Analytical (Fast, Pre-Compiled):** For robots with known closed-form IK solutions (most 6-DOF arms with a spherical wrist qualify), use **IKFast-generated code**. IKFast works by symbolically solving the IK equations for a specific URDF at build time, generating a C++ source file containing the closed-form solution. This is compiled into a shared library specific to that kinematic structure. At runtime, it returns up to 16 valid solutions in < 100 microseconds. **IKFast is NOT a general-purpose runtime solver** — it is precomputed per robot model offline.

        > *Ref: IKFast documentation — http://openrave.org/docs/0.8.2/openravepy/ikfast/*

    - **Tier 2 — Numerical (General, Handles Edge Cases):** For redundant manipulators (7+ DOF), robots without analytical solutions, or poses near singularities: use **Damped Least Squares (DLS)** Jacobian-based iteration. The update rule is:

        $$\Delta\theta = J^T(JJ^T + \lambda^2 I)^{-1} \cdot \Delta x$$

        where $\lambda$ is the damping factor. Seed the solver with the cached solution from the last successful IK call (warm-starting for faster convergence).

- **Singularity Handling (Critical — Original Benchmark Did Not Cover This):**

    A **kinematic singularity** occurs when the Jacobian matrix $J$ loses rank — two or more joint axes align, reducing the robot's instantaneous degrees of freedom. At a singularity, the standard Jacobian inverse produces infinitely large (or numerically explosive) joint velocities.

    The three canonical singularity types for a 6-DOF serial manipulator:
    - **Shoulder singularity:** Wrist center lies directly above/below the shoulder joint.
    - **Elbow singularity:** Arm is fully extended or fully folded.
    - **Wrist singularity:** Two wrist joint axes become co-linear (common in spherical wrists when the middle wrist joint is near 0 degrees).

    **Detection:** Before executing any IK result, compute the **manipulability index** $w = \sqrt{\det(JJ^T)}$. If $w < w_{threshold}$ (typically 0.01 for normalized Jacobians), the requested pose is near a singularity. Return a warning to the caller and optionally project the target pose slightly away from the singularity manifold.

    **Mitigation via DLS:** The damping term $\lambda$ in Damped Least Squares prevents unbounded joint velocities near singularities. $\lambda$ should be made **adaptive** — scale $\lambda$ inversely with the minimum singular value of $J$ (large damping near singularities, small damping far from them). This is the Nakamura-Hanafusa approach.

    > *Ref: Nakamura & Hanafusa, "Inverse Kinematic Solutions With Singularity Robustness" (1986) — canonical DLS reference*
    > *Ref: Siciliano et al., "Robotics: Modelling, Planning and Control" (Springer), Chapter 3*

- **Joint Limit Constraints:** Every IK solution must be validated against joint position limits, velocity limits, and (for real-time servoing) jerk limits. A solution that is geometrically valid but requires an instantaneous velocity jump is not a physically executable solution.

#### Architecture (UML)
![Architecture Diagram](diagram_q2.png)

---

## Question 3: Collaborative Mapping and Anomaly Detection Pipeline

### Problem

Your company is deploying autonomous exploration robots to map highly unstructured, dynamically changing subterranean environments.

**Part A (SLAM vs Model, ~15 min)**
For edge navigation, the robots must localize themselves. Discuss the trade-offs between traditional geometric SLAM (Simultaneous Localization and Mapping) versus learned, end-to-end Neural Network models. When would you use one over the other?

**Part B (VAE Classes, ~15 min)**
To build a global topological map, the cloud needs to analyze the camera streams being ingested. Explain how you would use Variational Autoencoders (VAEs) to process these images. What is a latent space, and why are VAEs specifically useful here compared to standard autoencoders?

**Part C (Clustering for Anomaly Detection, ~15 min)**
Given the output from the VAE, design a system using clustering to automatically identify "anomalous" or "novel" environments that the robots discover, flagging them for human review.

---

### A+ Response Benchmark

#### Part A — SLAM vs. Learned Models

- **Traditional Geometric SLAM (e.g., ORB-SLAM3, LIO-SAM, Cartographer):**
    - *Pros:* Mathematically guaranteed consistency via pose graph optimization and loop closure. Explainable — every keyframe, feature match, and graph edge can be inspected. Runs fast on CPUs. Highly accurate in texture-rich, static environments.
    - *Cons:* Fails in featureless corridors, shiny/reflective surfaces, and dynamic scenes (moving people, machinery). The critical failure mode is **loop closure failure in perceptually aliased environments** — long corridors where different locations look identical to the feature extractor. Without correct loop closures, the robot's pose estimate drifts without bound over long traversals.

- **Learned Models (e.g., Visual Odometry via CNNs/Transformers, End-to-End SLAM):**
    - *Pros:* Resilient to poor lighting, motion blur, featureless terrain, and dynamic obstacles, because they learn semantic priors from training data rather than relying on hand-crafted feature extraction.
    - *Cons:* Opaque failure modes (no geometric consistency guarantee). Computationally heavy (requires edge GPU/NPU). Fails silently out-of-distribution — a model trained on indoor warehouse data will produce confident but wrong predictions in an underground cave.

- **A+ Conclusion — Hybrid Architecture with Specific Coupling Mechanism:**

    Use a geometric SLAM system (ORB-SLAM3 for visual, LIO-SAM for lidar-inertial) as the **primary state estimator**. Augment it with a learned place recognition model (e.g., **NetVLAD** — a CNN that produces compact global image descriptors) for **loop closure detection**.

    **How the coupling works:** The learned module runs in parallel, producing a global descriptor for each keyframe. When the descriptor's cosine similarity to a historical keyframe exceeds a threshold, it proposes a loop closure candidate to the SLAM backend. The SLAM backend validates the candidate via a **geometric consistency check** (e.g., compute a relative pose estimate from feature matches and verify it against the current pose graph via a chi-squared test on the Mahalanobis distance). If consistent, the loop closure is integrated into the pose graph; if not, it is rejected. This preserves mathematical consistency while gaining semantic loop closure capability.

    > *Ref: Arandjelovic et al., "NetVLAD: CNN architecture for weakly supervised place recognition" (2016) — https://arxiv.org/abs/1511.07247*
    > *Ref: Cadena et al., "Past, Present, and Future of SLAM" (IEEE T-RO 2016) — https://arxiv.org/abs/1606.05830*
    > *Ref: Campos et al., "ORB-SLAM3" (2021) — https://arxiv.org/abs/2007.11898*

---

#### Part B — VAE Classes and Latent Space

- **VAE Concept:** A Variational Autoencoder trains an encoder network $q_\phi(z|x)$ that maps a raw image $x$ (e.g., a 1080p camera frame — a high-dimensional vector) to a probability distribution over a low-dimensional **latent space** $z \in \mathbb{R}^d$ (typically $d$ = 64-256). A decoder network $p_\theta(x|z)$ reconstructs the original image from $z$.

- **The Mechanism (KL Divergence) — Why VAE and Not a Standard Autoencoder:**

    The encoder outputs not a single vector but the parameters of a Gaussian: mean $\mu$ and log-variance $\log\sigma^2$. The latent vector is sampled via the **reparameterization trick**: $z = \mu + \sigma \cdot \epsilon$, where $\epsilon \sim \mathcal{N}(0, I)$ (this makes backpropagation through the sampling step possible).

    The training loss is the **Evidence Lower Bound (ELBO):**

    $$\mathcal{L} = \underbrace{\mathbb{E}[\log p_\theta(x|z)]}_{\text{Reconstruction quality}} - \underbrace{D_{KL}(q_\phi(z|x) \| \mathcal{N}(0, I))}_{\text{Latent space regularization}}$$

    The first term measures reconstruction quality (how well does the decoder reproduce the input?). The second term — the **KL divergence** — regularizes the latent space by penalizing encodings that deviate from a standard normal distribution. This is what makes VAEs different from standard autoencoders:

    Without KL regularization (a plain autoencoder), the encoder collapses to memorized point embeddings with empty, discontinuous regions between them. Interpolation and clustering in this space are meaningless. With KL regularization, visually and semantically similar inputs are forced to map to nearby, continuous regions in latent space — which is a prerequisite for meaningful downstream clustering.

    A candidate who says "VAEs produce structured latent spaces" without explaining *why* (the KL term in the ELBO) is pattern-matching the answer without understanding it.

    > *Ref: Kingma & Welling, "Auto-Encoding Variational Bayes" (2013) — https://arxiv.org/abs/1312.6114*

- **Deployment Note:** At inference time (on the robot), only the encoder is needed — the decoder is used only during training. The encoder backbone should be lightweight for edge deployment (MobileNetV2, EfficientNet-Lite), fine-tuned on in-domain subterranean imagery.

---

#### Part C — Clustering for Anomaly Detection

- **Why Not Batch K-Means with Fixed K:**

    The question is set in an **open-world exploration** context where the number of distinct terrain types ($K$) is unknown a priori and grows as robots discover new environments. Standard batch K-Means requires pre-specifying $K$, which is fundamentally incompatible with this problem. A candidate who proposes batch K-Means without acknowledging this limitation is missing a key architectural constraint.

    **Correct alternatives:**
    - **HDBSCAN (Hierarchical Density-Based Spatial Clustering of Applications with Noise):** Discovers clusters of arbitrary shape, does not require pre-specifying $K$, and naturally produces an "outlier" label for points that don't belong to any dense cluster — which is exactly the anomaly signal needed. HDBSCAN is preferred over DBSCAN for its stability across different density scales.
    - **Incremental codebook approach:** Start with an empty set of centroids. When a new latent vector arrives and `dist(z, nearest_centroid) > θ_new_cluster`, create a new centroid. This is essentially growing K-Means.
    - **Online clustering variants** (DBSTREAM, DenStream) for true streaming data, maintaining cluster summaries without full re-clustering.

    > *Ref: Campello et al., "Density-Based Clustering Based on Hierarchical Density Estimates" (HDBSCAN, 2013) — https://link.springer.com/chapter/10.1007/978-3-642-37456-2_14*
    > *Ref: McInnes et al., HDBSCAN library — https://hdbscan.readthedocs.io/*

- **Anomaly Scoring:**

    For each incoming latent vector $z$, compute the distance to the nearest cluster centroid (or, for HDBSCAN, the outlier score). If the distance exceeds an anomaly threshold $\theta_{anomaly}$, flag for human review.

    **Distance metric in high dimensions (Curse of Dimensionality):** Euclidean distance becomes less discriminative in high-dimensional spaces (128-D). Two mitigation strategies:
    1. **Use cosine similarity** instead of L2 distance — it normalizes for magnitude, so images with similar semantic content but different exposure levels are correctly identified as related.
    2. **UMAP dimensionality reduction** as preprocessing: reduce 128-D latent vectors to 10-20D while preserving local and global topology. Clustering and distance computation in 10-D is dramatically better-behaved.
    3. **Constrain the VAE latent dimension:** For terrain classification with ~10-20 expected terrain types, a 32-64D latent space is typically sufficient and better-conditioned than 128-D.

    > *Ref: McInnes et al., "UMAP" (2018) — https://arxiv.org/abs/1802.03426*

- **Adaptive Thresholding:** A static $\theta_{anomaly}$ value drifts as the model improves (all distances shrink as the VAE learns better representations). Use a **percentile-based adaptive threshold**: flag the top $P$% of anomaly scores in a rolling window (e.g., top 2% of the last 10,000 vectors). This is distribution-free and self-calibrating.

- **Active Learning Feedback Loop:** When a human reviewer labels a flagged vector as "genuinely novel terrain" (not a sensor glitch), that vector and its $K$ nearest neighbors are added to the labeled training set. The VAE is periodically fine-tuned with this new data to improve its representation of rare terrains, closing the active learning loop.

#### Architecture (UML)
![Architecture Diagram](diagram_q3.png)

---

## Question 4: Quality-Aware Data Ingestion Pipeline for AEB Resimulation

### Problem

Your ADAS engineering team runs massive cloud resimulations on fleet data to validate Automated Emergency Braking (AEB). Currently, 70% of GPU simulation jobs crash at runtime because the supposedly "valid" driving logs actually contain silent failures (e.g., missing 50 Hz CAN signals, empty log boundaries, or missing radar topics).

**Part A (Failure Modes, ~10 min)**
Explain why validating data upload success at the file level is insufficient for active safety resimulation. What are the common data failure modes in vehicle logs that cause simulation stacks to crash?

**Part B (Quality Metrics Architecture, ~20 min)**
Design a quality-aware ingestion pipeline. How do you architect a system to ingest petabytes of ROS bags, extract quality metrics per segment, and make them queryable before kicking off a simulation stack?

**Part C (Algorithm, ~15 min)**
Describe the specific metrics you would compute per segment to detect these data gaps. How do you implement "chain detection" to group consecutive valid segments and recover intervals from otherwise broken log files?

---

### A+ Response Benchmark

#### Part A — Failure Modes

- **File vs. Signal Validation:** The candidate must distinguish between **file-level integrity** (is the MCAP index parseable? is the file uncorrupted?) and **signal-level integrity** (is the specific `vehicle_dynamics/imu` topic present continuously at its expected frequency?). File-level validation is necessary but grossly insufficient.

- **The Four Failure Modes:** A+ candidates identify all four:

    1. **Signal gaps:** A required topic (e.g., drive-by-wire IMU at 50 Hz) drops out for 2 seconds mid-drive during a high-dynamic maneuver. The AEB's Time-to-Collision (TTC) calculator requires continuous IMU data; a 2-second gap produces an invalid TTC estimate and crashes the simulation.

    2. **Empty boundaries:** At vehicle startup and shutdown, sensors go through initialization/calibration sequences. The log records these periods, but the sensor data is invalid (IMU calibrating, camera auto-exposing, radar spinning up). Simulations run on boundary segments produce nonsense results even though all topics are technically "present."

    3. **Missing required topics:** A drive log has perfect camera and IMU data, but the radar driver crashed and produced zero messages. AEB requires both camera and radar for long-range detection; this log cannot be used for AEB validation regardless of other signal health.

    4. **Schema mismatches (often missed):** Over the lifetime of a multi-year ADAS fleet, firmware updates and software refactors change message schemas. A `radar/tracks` topic from a 2022 vehicle may have a `track_id` field; the same topic from a 2024 vehicle may have renamed it to `object_id`. The simulation stack compiled against the 2024 schema will silently misparse 2022 logs — not a crash, but subtly wrong results that corrupt validation outcomes. The ingestion pipeline must validate each topic's recorded schema hash (from the MCAP schema record or ROS msg MD5) against the expected schema for the target simulation stack version.

        > *Ref: MCAP schema records — https://mcap.dev/spec#schema-op*

- **Safety Criticality:** In active safety testing, the simulation stack cannot "guess" or interpolate missing data. The simulation MUST fail if required inputs are absent or degraded — silent degradation produces false safety validation results, which is worse than a crash.

---

#### Part B — Quality Metrics Architecture

- **Shift-Left Principle:** Quality assessment must move from *resimulation time* (where failures waste GPU hours) to *ingestion time* (where they're cheap to detect and filter).

- **The Ingestion Pipeline:**

    Raw MCAP files are uploaded to object storage (S3 or GCS). An ingest trigger (S3 event notification → SQS → Lambda, or Kafka topic) launches a Spark job per file.

    The Spark job executes four steps:
    1. **Parses the MCAP index** — extracts topic list, schema hashes, start/end timestamps. If the index is corrupt, the entire file is rejected immediately (fast fail — no further processing).
    2. **Validates schemas** — checks each required topic's recorded schema hash against a **schema registry** (a key-value store mapping `{topic_name, simulation_stack_version} → expected_schema_hash`). Mismatches are flagged as `schema_mismatch = TRUE`.
    3. **Chunks the file** into fixed-size segments (30 seconds is appropriate — long enough for meaningful driving scenarios, short enough for fine-grained gap recovery).
    4. **Computes quality metrics per segment** (see Part C).

    Metric records are written to an Apache Hudi (or Delta Lake) table partitioned by `(vehicle_id, date, simulation_stack_version)`. This enables efficient filtering by date range and stack version.

    > *Ref: Confluent Schema Registry (conceptual analogue for Kafka) — https://docs.confluent.io/platform/current/schema-registry/index.html*

- **The Pre-Flight Gate:** Before a GPU simulation job is allocated, the orchestrator (Airflow, Prefect, or custom) runs a validation query:

    ```sql
    SELECT segment_id, start_ts, end_ts
    FROM segment_quality_metrics
    WHERE vehicle_id = :vid
      AND simulation_stack_version = :stack_ver
      AND schema_mismatch = FALSE
      AND imu_max_gap_s <= 0.1
      AND imu_fill_rate >= 0.95
      AND radar_message_count > 0
      AND camera_message_count > 0
      AND is_boundary_segment = FALSE
    ORDER BY start_ts
    ```

    Only segments passing all predicates are submitted to the GPU pool. This moves the 70% crash rate to effectively 0% by never submitting invalid data.

---

#### Part C — Algorithm: Metrics and Chain Detection

- **Three Metrics Per Topic Per Segment (Not Two):**

    The original two-metric approach (`message_count` and `max_inter_message_time_delta`) misses a specific failure mode: **intermittent dropouts that individually fall below the gap threshold but cumulatively represent significant data loss**. For example, a 50 Hz IMU that drops one message every 0.5 seconds (below a 0.5s gap threshold) will have only 1,350 messages in a 30-second segment instead of 1,500 — a 10% loss that the two-metric system labels "valid."

    The correct metric set:

    | Metric | Formula | Purpose |
    |---|---|---|
    | `message_count` | `COUNT(msgs)` where topic = T in segment | Detects completely absent topics |
    | `max_gap_s` | `MAX(t[i+1] - t[i])` for consecutive messages | Detects burst dropout events |
    | `fill_rate` | `message_count / (segment_duration_s × expected_hz)` | Detects chronic low-rate degradation |

    A segment is valid for topic T if all three pass:
    - `message_count > 0`
    - `max_gap_s <= gap_threshold[T]` (topic-specific: 0.1s for IMU, 1.0s for radar, 0.5s for GPS)
    - `fill_rate >= 0.95`

    The `expected_hz` for each topic is stored in the schema registry or a topic configuration table.

- **Chain Detection Algorithm:**

    ```python
    def find_valid_chains(
        segments: List[Segment],
        required_topics: List[str]
    ) -> List[Chain]:
        """
        segments: sorted by start_ts, fixed-size (e.g., 30s each)
        Returns: list of maximal consecutive chains of valid segments
        """
        valid = [
            s for s in segments
            if all(s.is_valid(t) for t in required_topics)
        ]

        chains = []
        current_chain = []

        for seg in valid:
            if not current_chain:
                current_chain.append(seg)
            elif seg.index == current_chain[-1].index + 1:
                # Consecutive — extend chain
                current_chain.append(seg)
            else:
                # Gap in segment indices — chain is broken
                chains.append(Chain(current_chain))
                current_chain = [seg]

        if current_chain:
            chains.append(Chain(current_chain))

        return [c for c in chains if c.duration_s >= MIN_CHAIN_DURATION_S]
    ```

- **Interval-Based Recovery:** Without interval recovery, a 1-hour log with a single 5-minute bad segment at t=30min yields zero valid simulation jobs (0% yield). With chain detection and interval recovery, it produces two independent simulation jobs — one covering [0, 30min) and one covering [35min, 60min) — a 92% yield from the same data.

    Across a large fleet where 30% of logs have at least one bad segment, interval recovery moves usable data yield from ~70% to ~95% (only logs where bad segments cluster at the boundaries or are so frequent that no chain reaches minimum duration remain unusable).

- **Boundary Segment Exclusion:** The first and last segments of any drive log should be automatically flagged `is_boundary_segment = TRUE` and excluded from simulation. Sensor startup/shutdown sequences contaminate these segments with initialization artifacts that will break simulation stacks expecting steady-state sensor inputs.

#### Architecture (UML)
![Architecture Diagram](diagram_q4.png)
