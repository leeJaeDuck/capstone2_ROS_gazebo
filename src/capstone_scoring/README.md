# Changing Animal Picture 

In terminal:

```
rosrun capstone_scoring animal_topic.py
```

- After putting a ball into the goal. 
Publish to /current_ball topic, 1 or 2 depending on the number of goal-ins you have.

- For different order of animal picutre, choose case value in the animal_topic.py
cases : 1 or 2 or 3

- Randomly Relocating an object in the entrance zone

---

# Randomly Locating Stop Sign

In terminal:

```
rosrun capstone_scoring stop.py
```
- Change the values in line 14 of stop.py

```python
goal_y =  np.random.uniform([lower bound],[upper bound])
```
