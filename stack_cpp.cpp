#include <stdlib.h>
#include <stdio.h>

extern "C" {

struct Node {
    int data;
    struct Node* next;
};

struct Stack {
    struct Node* top;
};

struct Stack* create_stack() {
    struct Stack* stack = (struct Stack*)malloc(sizeof(struct Stack));
    if (stack) stack->top = NULL;
    return stack;
}

void delete_stack(struct Stack* stack) {
    if (!stack) return;
    while (stack->top) {
        struct Node* temp = stack->top;
        stack->top = temp->next;
        free(temp);
    }
    free(stack);
}

int is_empty(struct Stack* stack) {
    return !stack || !stack->top;
}

int push(struct Stack* stack, int value) {
    if (!stack) return -1;
    struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
    if (!newNode) return -2;
    newNode->data = value;
    newNode->next = stack->top;
    stack->top = newNode;
    return 0;
}

int pop(struct Stack* stack, int* result) {
    if (!stack || is_empty(stack)) return -1;
    struct Node* temp = stack->top;
    *result = temp->data;
    stack->top = temp->next;
    free(temp);
    return 0;
}

int peek(struct Stack* stack, int* result) {
    if (!stack || is_empty(stack)) return -1;
    *result = stack->top->data;
    return 0;
}

int get_size(struct Stack* stack) {
    if (!stack) return 0;
    int count = 0;
    struct Node* current = stack->top;
    while (current) { count++; current = current->next; }
    return count;
}

int* get_all_elements(struct Stack* stack, int* size) {
    if (!stack) { *size = 0; return NULL; }
    *size = get_size(stack);
    if (*size == 0) return NULL;
    
    int* elements = (int*)malloc(*size * sizeof(int));
    if (!elements) return NULL;
    
    struct Node* current = stack->top;
    for (int i = 0; i < *size; i++) {
        elements[i] = current->data;
        current = current->next;
    }
    return elements;
}

void free_elements(int* elements) {
    if (elements) free(elements);
}

void clear_stack(struct Stack* stack) {
    if (!stack) return;
    while (stack->top) {
        struct Node* temp = stack->top;
        stack->top = temp->next;
        free(temp);
    }
}

}