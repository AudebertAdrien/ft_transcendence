import gym

# Check if the Atari environment is available
try:
    env = gym.make('ALE/Pong-v5')
    print("Atari environment is available.")
    env.close()
except gym.error.Error as e:
    print(f"Error: {e}")
