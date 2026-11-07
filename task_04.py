"""Task 04: Topological dependency planner with alphabetical tie-breaking."""

import heapq

def execution_order(tasks, dependencies):
    task_list = list(tasks)
    if len(set(task_list)) != len(task_list):
        raise ValueError("Duplicate task names are not allowed")

    task_set = set(task_list)
    outgoing = {task: set() for task in task_list}
    indegree = {task: 0 for task in task_list}

    for before, after in dependencies:
        if before not in task_set or after not in task_set:
            raise ValueError(f"Unknown task in dependency: ({before}, {after})")
        if after not in outgoing[before]:
            outgoing[before].add(after)
            indegree[after] += 1

    ready = [task for task in task_list if indegree[task] == 0]
    heapq.heapify(ready)
    result = []

    while ready:
        current = heapq.heappop(ready)
        result.append(current)
        for neighbor in sorted(outgoing[current]):
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                heapq.heappush(ready, neighbor)

    if len(result) != len(task_list):
        raise ValueError("Dependency cycle detected")
    return result


if __name__ == "__main__":
    print(execution_order(
        ["build", "test", "deploy"],
        [("build", "test"), ("test", "deploy")]
    ))
