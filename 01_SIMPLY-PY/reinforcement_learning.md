# REINFORCEMENT LEARNING

## Theoretical Foundations of Reinforcement Learning

### Markov Decision Process (MDP)

Markov process is the simplest child of the Markov family, which is also known as Markov chain. Imagine an observable system only by yourself, what you observe is called states, and the system can switch between the states. The set of the all possible states is known as state space. For Markov process, the number of possible states need to be finite. Also, the system can not be influenced by you but can be observe while it changing. 

For example, looking at the simplest model of the weather in some city, we can observe the current day as sunny or rainy, which is our state space. A sequence of observations over time forms a chain of states, such as [sunny, sunny, rainy, sunny, …], and this is called history.

To call such system an Markov Process, it need to fulfill the Markov Property, which means that the future system dynamics from any state have to depend on this state only. The main point of the Markov property is to make every observable state self-contained to describe the future of the system. In this chase, **only one state is required to model the future dynamics of the system and not the whole history** or, say, the last N states. 

As the system model complies with Markov property, you can capture transition probabilities with a transition matrix, which is a square matrix of the size N x N, where N is the number of states in our model. Every cell in a row, i, and a column, j, in the matrix contains the probability of the system to transition from state i to state j. The transition matrix defines the system dynamics. Additionally, Markov process implies stationarity, where there is no any factor influencing the system dynamics. 

A state transition graph, where circle represents the state, arrow represents the possible transitions and self revolving arrows represents the self-state. If a model is at coffee state, then its next state is only depends on the Coffee state not any state before it. 

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/df89fc0b-ce89-458c-88fa-b18c8cdb3e6b/03193b46-bb12-498f-911e-b8878f5c32e5/image.png)

In Markov reward processes, the Markov process is extended to a bit by adding the reward value to out transition from state to state. Reward is a another square matrix, similar to the transition matrix, with reward given for transitioning from state i to state j, which reside in row i and column j. 

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/df89fc0b-ce89-458c-88fa-b18c8cdb3e6b/36c08b38-3e68-463c-b123-bc5b6f007385/image.png)

The return (Gt) is the sum of rewards agent collects in future from the time ‘t’ onward. The discount factor (Gamma) is applied at every step starting from the point where we calculate the return Gt. The farther the reward is in time, the higher the power of Gamma, which means bigger discount. 

In RL, the agent uses these rewards to calculate:

1. **Immediate reward** (R) for each step.
2. **Return** (Gt) by summing up discounted future rewards.
3. **Value function** (V(s)) to average the returns for a state.

The State Value [V(s)] is the average return obtained from the Markov reward processes. The equation of the state value is given as: 

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/df89fc0b-ce89-458c-88fa-b18c8cdb3e6b/ad74b21c-9945-4fbe-b64f-d5260391d76c/image.png)

This equation simply represents, **“ If I start at state s, what is the average total reward I can expect over time?”**

V(s) quantifies how **good** a state s is in terms of long-term rewards. In RL, this concept is extended to find the optimal policies that maximize V(s)

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/df89fc0b-ce89-458c-88fa-b18c8cdb3e6b/ad5a668d-8551-456f-bfbf-7deae856c754/image.png)

In the absence of terminal states (sink states) in infinite horizon problems, the value of Gamma = 1, the agent becomes completely far-sighted and cares about all the future rewards equally, no matter how far they are in the future which leads the agent to sums all future rewards infinitely.

The value of Gamma = 1 is idea for finite-horizon problems (tic-tac-toe) but impractical in infinite-horizon problems without a stopping condition. A larger gamma (e.g., 0.9 or 0.99) means the agent considers the **long-term future more**, but rewards farther in time still diminish in value.Gamma < 1 avoids the problem of infinite sums, which is common in infinite-horizon problems. 

---

### Policy

Policy is some set of rules that controls the agent’s behavior. The main objective of RL is to gather the maximum cumulative return as possible. Mathematically policy can be represented by the given equation, 

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/df89fc0b-ce89-458c-88fa-b18c8cdb3e6b/1306c345-53e4-4133-9b89-187b8c9f4f5e/image.png)

where ‘|’ denotes the conditional probability, P denotes the probability, At denotes the action ‘a’ chosen by the agent at time step t, St denotes the state ‘s’ the agent currently in at time t. 

The equation basically ask, “ **If I am in state “s”, what action “a” should I take?”**

There are two different types of policy RL. 

1. Deterministic Policy where the action ‘a’ is chosen with certainty.
2. Stochastic Policy where the actions are chosen randomly based on the probability distribution. 

---

---

## Dynamic Programming and Bellman Equation

Dynamic programming consist of two different parts, dynamic and programming, the term dynamic means such problems with temporal or sequential aspect, and the programming means optimizing the policy, mathematically. 

Any problem to be solved with dynamic programming requires following property: 

1. Optimal substructure
2. Overlapping sub problems

These properties are satisfied by the MDP (Markov Decision Process) which allow the use of Bellman Optimality equation to creates the recursive decomposition to the problem. 

---

Bellman Equation of Optimality applies for two different cases: 

1. Deterministic Case
2. Stochastic Case

### Deterministic Case for Bellman Equation of Optimality

Deterministic cases are such problems with where the actions have 100% guaranteed outcome and not influenced by randomness.. The equation for the deterministic case is given by: 

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/df89fc0b-ce89-458c-88fa-b18c8cdb3e6b/d8de4770-54a2-4451-828b-f7c7791dabdd/image.png)

Here:

- ( V^*(s) ) is the optimal value function for state ( s ).
- ( R(s, a) ) is the reward received after taking action ( a ) in state ( s ).
- ( \gamma ) is the discount factor, which determines the importance of future rewards.
- ( s' ) is the next state resulting from taking action ( a ) in state ( s ).

### Stochastic Case for Bellman Equation of Optimality

The outcomes of the actions are governed by the probabilities in the stochastic cases of Bellman Optimality equation. This means that taking an action in a given state can lead to multiple possible next states, each with certain probability. 

The equation for the stochastic case is given as: 

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/df89fc0b-ce89-458c-88fa-b18c8cdb3e6b/e8db5520-6b2f-498b-9a21-83f9b9d92829/image.png)

Here:

- ( V^*(s) ) is the optimal value function for state ( s ).
- ( R(s, a) ) is the expected reward received after taking action ( a ) in state ( s ).
- ( \gamma ) is the discount factor, which determines the importance of future rewards.
- ( P(s' | s, a) ) is the probability of transitioning to state ( s' ) from state ( s ) after taking action (a).
- ( s' ) represents the possible next states.
- 

### Q(s,a) & V(s)

Q(s,a) is known as the Q-value function whereas the V(s) is known as value function. They have the given mathematical connection with each other: 

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/df89fc0b-ce89-458c-88fa-b18c8cdb3e6b/ee9b6fec-56ac-43c8-9e68-7fecad2cd460/image.png)

The key difference between Q(s,a) and V(s) lies in what they evaluate:

- **V(s) - State Value Function:** Represents the expected return starting from state s and following the current policy. It tells us how good it is to be in a particular state.
- **Q(s,a) - State-Action Value Function:** Represents the expected return starting from state s, taking action a, and then following the current policy. It tells us how good it is to take a specific action in a particular state.

The relationship between Q(s,a) and V(s) can be expressed as:

V(s) = max Q(s,a) for all actions **a**

This means the value of a state is equal to the maximum Q-value possible from that state across all possible actions.

### Bellman Equation for General Case

According to Bellman's optimality proof, at every state the agent ends up in, it needs to select the action with the maximum expected reward, which is a sum of the immediate reward and the one-step discounted long-term reward.

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/df89fc0b-ce89-458c-88fa-b18c8cdb3e6b/3553e82c-6346-485a-997a-c526cfc31de4/image.png)

Representation of Q(s,a) recursively: 

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/df89fc0b-ce89-458c-88fa-b18c8cdb3e6b/357aad7a-4bf7-4c32-a859-02d1fcc8045e/image.png)

## Value Iteration Method