package main

import "fmt"

type GCounter struct {
	ID    int
	State map[int]int
}

func NewGCounter(id int) *GCounter {
	state := make(map[int]int)
	state[id] = 0
	return &GCounter{ID: id, State: state}
}

// Increment the CRDT state via this GCounter.
func (g GCounter) increment() {
	g.State[g.ID] += 1
	// todo: publish
}

// Request the current global CRDT "value", or sum of counts across nodes
func (g GCounter) value() int {
	value := 0
	for _, count := range g.State {
		value += count
	}
	return value
}

// Merge a received state into our internal state.
func (g GCounter) join(state map[int]int) {
	for id, count := range state {
		val, ok := g.State[id]
		// update count to the max of the received & existing count
		if ok {
			g.State[id] = max(count, val)
		} else {
			g.State[id] = count
		}
	}
}

// Return the maximum of two integers.
func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}

func main() {
	node := *NewGCounter(1)
	fmt.Println(node.ID)
	fmt.Println(node.State)
	node.increment()
	fmt.Println(node.State)

	node2 := *NewGCounter(2)
	node2.increment()
	node2.increment()
	node2.increment()

	node.join(node2.State)
	fmt.Println(node.State)
}
