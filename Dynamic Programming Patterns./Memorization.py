def solve(params):
    memo = {}

    def dp(state):
        if state in memo:
            return memo[state]
        ans = 0  
        memo[state] = ans
        return ans

    return dp(initial_state)
