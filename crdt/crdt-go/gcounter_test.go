package main

import (
	"testing"
)

type DummyPubSub struct{}

func (ps *DummyPubSub) publish(id int, state map[int]int) {
}

func (ps *DummyPubSub) subscribe(n Node) {
}

// Calls NewGCounter, checking for expected ID and presence of initial state
// for this node.
func TestNewGCounter(t *testing.T) {
	ps := &DummyPubSub{}

	id := 3
	node := *NewGCounter(id, ps)

	// Check id is set correctly
	if node.ID != id {
		t.Fatalf(`NewGCounter(%d).ID = %d, should be %d`, id, node.ID, id)
	}

	// Check initial state is set to 0 for this node. (Non-opinionated on whether
	// it is set for other nodes.)
	expectCountAtNode(t, &node, 0)
}

// Calls GCounter.increment, checking that the state is incremented at the
// correct node as expected. (Non-opinionated on whether the nodes are
// converged with each other.
func TestGCounterIncrement(t *testing.T) {
	ps := &DummyPubSub{}
	node0 := *NewGCounter(0, ps)
	node1 := *NewGCounter(1, ps)

	// Increment node0. node0 should increment its own count, while node1 should
	// not change its own count.
	node0.increment()
	expectCountAtNode(t, &node0, 1)
	expectCountAtNode(t, &node1, 0)

	// Same but increment at node1.
	node1.increment()
	expectCountAtNode(t, &node0, 1)
	expectCountAtNode(t, &node1, 1)

	// Increment once more at node0.
	node0.increment()
	expectCountAtNode(t, &node0, 2)
	expectCountAtNode(t, &node1, 1)
}

// Helper function to test for an expected count value at this node.
func expectCountAtNode(t *testing.T, node *GCounter, expected int) {
	if val, ok := node.State[node.ID]; ok {
		if val == expected {
			return // passed
		}
		t.Fatalf(`State[%d] = %d; expected %d`, node.ID, val, expected)
	}
	t.Fatalf(`Unable to retrieve State[%d] from node %d`, node.ID, node.ID)
}
