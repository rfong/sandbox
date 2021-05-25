package main

import "fmt"

// Interface for a node object that has a UID and can receive state updates
type Node interface {
	getID() int
	join(map[int]int) // callable to receive a state update
}

// Interface for publishing state updates to Node subscribers.
type PubSubInterface interface {
	publish(int, map[int]int)
}

// GCounter is a grow-only counter that satisfies the Node interface.
type GCounter struct {
	ID     int
	State  map[int]int
	PubSub PubSubInterface
}

// NodeManager communicates between Nodes and satisfies the PubSub interface.
type NodeManager struct {
	Nodes     map[int]Node
	maxIDSeen int // not guaranteed to currently be in Nodes
}

// Instantiate NodeManager state
func NewNodeManager() *NodeManager {
	return &NodeManager{maxIDSeen: -1, Nodes: make(map[int]Node)}
}

// Create and return a new GCounter node with autoincrementing ID
func (nm *NodeManager) newNode() *GCounter {
	// Create a GCounter with new unique ID and reference to NodeManager
	n := NewGCounter(nm.maxIDSeen+1, nm)
	// Increment our max ID seen to match
	nm.maxIDSeen++
	// Track in our list of Nodes
	nm.Nodes[n.ID] = n
	return n
}

// Sends out a state update to all tracked Nodes.
func (nm *NodeManager) publish(senderID int, state map[int]int) {
	for _, node := range nm.Nodes {
		if node.getID() != senderID { // We can skip publishing to the sender
			node.join(state)
		}
	}
}

// Instantiate GCounter state
func NewGCounter(id int, pubsub PubSubInterface) *GCounter {
	state := make(map[int]int)
	state[id] = 0
	return &GCounter{ID: id, State: state, PubSub: pubsub}
}

// getID() method to satisfy the Node interface.
func (g *GCounter) getID() int {
	return g.ID
}

// Increment the CRDT state via this GCounter node.
func (g *GCounter) increment() {
	// Increment this node's state
	g.State[g.ID] += 1
	// Publish to others
	fmt.Printf("\nNode %d increment()\n", g.ID)
	g.PubSub.publish(g.ID, g.State)
}

// Request the current global CRDT "value", or sum of known counts in state
func (g *GCounter) value() int {
	value := 0
	for _, count := range g.State {
		value += count
	}
	return value
}

// Merge a received state into our internal state.
func (g *GCounter) join(state map[int]int) {
	for id, count := range state {
		val, ok := g.State[id]
		// update count to the max of the received & existing count
		if ok {
			g.State[id] = max(count, val)
		} else {
			g.State[id] = count
		}
	}
	fmt.Printf("Node %d state: %v\n", g.ID, g.State)
}

// Return the maximum of two integers.
func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}

// Sandbox
func main() {
	nm := NewNodeManager()

	node0 := nm.newNode()
	fmt.Println(node0.ID)
	fmt.Println(node0.State)
	node0.increment()
	fmt.Println(node0.State)

	node1 := nm.newNode()
	node1.increment()
	node1.increment()

	node0.increment()
}
