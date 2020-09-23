// C++ program to rearrange a linked list in such a
// way that all odd positioned node are stored before
// all even positioned nodes
#include<bits/stdc++.h>
using namespace std;

// Linked List Node
struct Node
{
    int data;
    struct Node* next;
};

// A utility function to create a new node
Node* newNode(int key)
{
    Node *temp = new Node;
    temp->data = key;
    temp->next = NULL;
    return temp;
}

// Rearranges given linked list such that all even
// positioned nodes are before odd positioned.
// Returns new head of linked List.
void rearrangeEvenOdd(Node **head)
{
    // Corner case
    if (*head == NULL || (*head)->next==NULL||(*head)->next->next==NULL)
        return;

    // Initialize first nodes of even and
    // odd lists
    Node *odd = *head;
    Node *even = (*head)->next;
    Node *evenfrst = even;
    Node *lastodd;


    // traverse till we get both odd and even positioned lists in pairs
    while(odd->next->next && even->next->next)
    {
        odd->next=even->next;
        odd=even->next;
        lastodd=even->next;
        even->next=odd->next;
        even=odd->next;
    }

     // if a single odd positioned node is left
    if(odd->next->next != NULL)
    {
        odd->next=even->next;
        odd=even->next;
        lastodd=even->next;
        even->next=NULL;

    }

  // join the end of odd positioned list to the beginning of even list
    odd->next=evenfrst;
    
    Node *pr=lastodd;
    Node *ne=lastodd;
    Node *curr=evenfrst;
    
    while(curr != NULL)
    {
        ne=curr->next;
        curr->next=pr;
        pr=curr;
        curr=ne;
    }
    return;
}

// A utility function to print a linked list
void printlist(Node * node)
{
    while (node != NULL)
    {
        cout << node->data << "->";
        node = node->next;
    }
    cout << "NULL" << endl;
}

// Driver code
int main(void)
{
    Node *head = newNode(1);
    head->next = newNode(2);
    head->next->next = newNode(3);
    head->next->next->next = newNode(4);
    head->next->next->next->next = newNode(5);
    head->next->next->next->next->next = newNode(6);

    cout << "Given Linked List\n";
    printlist(head);

    rearrangeEvenOdd(&head);

    cout << "\nModified Linked List\n";
    printlist(head);

    return 0;
}