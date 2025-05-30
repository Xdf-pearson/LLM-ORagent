### 1. 基本车辆路径问题（VRP）

#### 问题描述：
给定一组客户点、车辆容量、车辆数量、起始点和终点，目标是找到使得所有客户点都被访问一次的最短路径方案。基本车辆路径问题（Vehicle Routing Problem，VRP）的数学模型可以使用整数线性规划（Integer Linear Programming，ILP）来表示。

#### 参数：
- \( n \)：客户点的数量（不包括起始点和结束点）。
- \( m \)：车辆的数量。
- \( c_{ij} \)：客户\( i \)到客户\( j \)的距离或运输成本，强调！其中设客户点 \( i \) 到客户点 \( i\) 自己的距离或成本为M。

#### 决策变量：
- \( x_{ij}^k \)：若车辆\( k \)从客户\( i \)到客户\( j \)，则 \( x_{ij}^k = 1 \)，否则为0。
- \( u_i \)：客户点\( i \)的“位置编号”，用于MTZ子环消除。

#### 目标函数：
\[
\min \sum_{k=1}^{m} \sum_{i=0}^{n} \sum_{j=0}^{n} c_{ij} \cdot x_{ij}^k
\]

#### 约束条件：
1. 每个客户必须被访问一次：
   \[
   \sum_{k=1}^{m} \sum_{j=1}^{n} x_{ij}^k = 1, \quad \forall i = 1, 2, \dots, n
   \]
2. 每辆车的路径必须从起始点出发，并最终返回终点：
   \[
   \sum_{j=1}^{n} x_{0j}^k = 1, \quad \forall k = 1, 2, \dots, m
   \]
   \[
   \sum_{i=1}^{n} x_{i0}^k = 1, \quad \forall k = 1, 2, \dots, m
   \]
3. 每辆车的路径是连续的：
   \[
   \sum_{j=1}^{n} x_{ij}^k = \sum_{j=1}^{n} x_{ji}^k, \quad \forall i = 1, 2, \dots, n, \forall k = 1, 2, \dots, m
   \]
4. **MTZ子环消除约束**：
   - 引入新的决策变量 \( u_i \)，表示客户点\( i \)的访问顺序。
   - 子环消除约束确保车辆的路径没有形成子环，\( u_i \geq 0 \)：
   \[
   u_i - u_j + (n + 1) \cdot x_{ij}^k \leq n, \quad \forall i = 1, \dots, n, \forall j = 2, \dots, n, \forall k = 1, \dots, m
   \]
   - \( u_i \geq 0, \quad \forall i = 1, \dots, n \)
5. Binary (0-1)约束：
   \[
   x_{ij}^k \in \{0, 1\}, \quad \forall i, j = 0, 1, \dots, n, \forall k = 1, 2, \dots, m
   \]

---

### 2. 带容量约束的车辆路径问题（CVRP）

#### 问题描述：
在CVRP问题中，目标是找到一种车队分配方案，使得每辆车都从一个起始点出发，途经访问每个客户点，并最终返回起始点，同时满足容量约束和最小化车辆的总行驶距离或成本。

#### 参数：
- \( n \)：客户点的数量（不包括起始点）。
- \( m \)：车辆的数量。
- \( Q \)：每辆车的容量限制。
- \( d_i \)：客户点 \( i \) 的需求量。
- \( c_{ij} \)：客户点 \( i \) 到客户点 \( j \) 的距离或成本,强调！其中设客户点 \( i \) 到客户点 \( i\) 自己的距离或成本为M。

#### 决策变量：
- \( x_{ij}^k \)：若车辆 \( k \) 从客户点 \( i \) 移动到客户点 \( j \)，则 \( x_{ij}^k = 1 \)，否则为 0。
- \( u_i \)：客户点\( i \)的“位置编号”，用于MTZ子环消除。

#### 目标函数：
最小化总行驶距离或成本：
\[
\text{Min} \quad \sum_{k=1}^{m} \sum_{i=0}^{n} \sum_{j=1}^{n} c_{ij} \cdot x_{ij}^k
\]

#### 约束条件：
1. 每个客户点必须访问一次且仅被访问一次：
   \[
   \sum_{k=1}^{m} \sum_{j=1}^{n} x_{ij}^k = 1, \quad \forall i = 1, \dots, n
   \]
2. 每辆车的路径必须从起始点开始，并在终点结束：
   \[
   \sum_{n=1}^{n} x_{0j}^k = 1, \quad \forall k = 1, \dots, m
   \]
   \[
   \sum_{i=1}^{n} x_{i0}^k = 1, \quad \forall k = 1, \dots, m
   \]
3. 车辆容量限制：
   \[
   \sum_{j=1}^{n} d_j \cdot x_{ij}^k \leq Q, \quad \forall i = 1, \dots, n, \quad \forall k = 1, \dots, m
   \]
4. **MTZ子环消除约束**：
   - 引入新的决策变量 \( u_i \)，表示客户点\( i \)的访问顺序。
   - 子环消除约束确保车辆的路径没有形成子环，\( u_i \geq 0 \)：
   \[
   u_i - u_j + (n + 1) \cdot x_{ij}^k \leq n, \quad \forall i = 1, \dots, n, \forall j = 2, \dots, n, \forall k = 1, \dots, m
   \]
   - \( u_i \geq 0, \quad \forall i = 1, \dots, n \)
5. Binary (0-1)约束：
   \[
   x_{ij}^k \in \{0, 1\}, \quad \forall i = 0, \dots, n, \quad \forall j = 0, \dots, n, \quad \forall k = 1, \dots, m
   \]

---

### 3. 带时间窗的车辆路径问题（VRPTW）

#### 问题描述：
在基本VRP的基础上，每个客户点都有一个时间窗，表示可以在某个时间范围内访问。目标是在满足时间窗和车辆容量限制的情况下，最小化总行驶距离或成本。

#### 参数：
- \( n \)：客户点的数量（不包括起始点）。
- \( m \)：车辆的数量。
- \( l_i \)：客户点 \( i \) 的需求量。
- \( e_i \)：客户点 \( i \) 的最早服务时间。
- \( l_i \)：客户点 \( i \) 的最晚服务时间。
- \( c_{ij} \)：客户点 \( i \) 到客户点 \( j \) 的距离或成本,强调！其中设客户点 \( i \) 到客户点 \( i\) 自己的距离或成本为M。

#### 决策变量：
- \( x_{ij}^k \)：若车辆 \( k \) 从客户点 \( i \) 移动到客户点 \( j \)，则 \( x_{ij}^k = 1 \)，否则为 0。
- \( u_i \)：客户点\( i \)的“位置编号”，用于MTZ子环消除。

#### 目标函数：
最小化总行驶距离或成本：
\[
\text{Min} \quad \sum_{k=1}^{m} \sum_{i=0}^{n} \sum_{j=0}^{n} c_{ij} \cdot x_{ij}^k
\]

#### 约束条件：
1. 每个客户点必须访问一次且仅被访问一次：
   \[
   \sum_{k=1}^{m} \sum_{j=1}^{n} x_{ij}^k = 1, \quad \forall i = 1, \dots, n
   \]
2. 每辆车的路径必须从起始点开始，并在终点结束：
   \[
   \sum_{j=1}^{n} x_{0j}^k = 1, \quad \forall k = 1, \dots, m
   \]
   \[
   \sum_{i=1}^{n} x_{i0}^k = 1, \quad \forall k = 1, \dots, m
   \]
3. 车辆容量限制：
   \[
   \sum_{j=1}^{n} d_j \cdot x_{ij}^k \leq Q, \quad \forall i = 1, \dots, n, \quad \forall k = 1, \dots, m
   \]
4. **MTZ子环消除约束**：
   - 引入新的决策变量 \( u_i \)，表示客户点\( i \)的访问顺序。
   - 子环消除约束确保车辆的路径没有形成子环，\( u_i \geq 0 \)：
   \[
   u_i - u_j + (n + 1) \cdot x_{ij}^k \leq n, \quad \forall i = 1, \dots, n, \forall j = 2, \dots, n, \forall k = 1, \dots, m
   \]
   - \( u_i \geq 0, \quad \forall i = 1, \dots, n \)
  
5. 时间窗约束：
   \[
   e_i \leq u_i \leq l_i, \quad \forall i = 1, \dots, n
   \]
6. Binary (0-1)约束：
   \[
   x_{ij}^k \in \{0, 1\}, \quad \forall i = 0, \dots, n, \quad \forall j = 0, \dots, n, \quad \forall k = 1, \dots, m
   \]


### 4.钢管切割问题数学模型

#### 问题描述：
某钢管零售商从钢管厂进货，将钢管按照顾客的需求切割后售出。现有客户对不同长度的钢管有需求，目标是最节省地切割19米长的原料钢管，满足顾客的需求，并最小化浪费。

#### 参数：
- \( L \)：原料钢管的长度。
- \( d_j \)：不同长度钢管的需求数量，\( j \in \{1, 2, \dots, n\} \)。
- \( m \)：可用的切割组合方案数量。
- \( a_{ij} \)：切割方案 \( i \) 提供的第 \( j \) 长度的钢管数量。

#### 决策变量：
- \( x_i \)：切割方案 \( i \) 使用的原料钢管数量，其中 \( i = 1, 2, \dots, m \)。
- \( a_{ij} \)：方案 \( i \) 提供的第 \( j \) 长度的钢管数量。

#### 目标函数：
最小化使用的19米钢管的数量：
\[
\min \sum_{i=1}^{m} x_i
\]
即最小化所有切割方案所使用的原料钢管数量。

#### 约束条件：
1. **满足不同长度钢管的需求**：
   \[
   \sum_{i=1}^{m} a_{ij} \cdot x_i \geq d_j, \quad \forall j = 1, 2, \dots, n 
   \]
   对于每种钢管长度，确保满足需求。

2. **切割方案的非负约束**：
   \[
   x_i \geq 0, \quad x_i \in \mathbb{Z}^+, \quad \forall i = 1, 2, \dots, m
   \]
   确保每个切割方案的数量为非负整数。

