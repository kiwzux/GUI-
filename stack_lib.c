#include <stdlib.h>
#include <stdio.h>

struct Node {
    int data;
    struct Node* next;
};

struct Stack {
    struct Node* top;
};

#ifdef _WIN32
    #define EXPORT __declspec(dllexport)
#else
    #define EXPORT
#endif

EXPORT struct Stack* create_stack() {
    struct Stack* stack = (struct Stack*)malloc(sizeof(struct Stack));
    if (stack != NULL) {
        stack->top = NULL;
    }
    return stack;
}

EXPORT void delete_stack(struct Stack* stack) {
    if (stack == NULL) return;
    
    while (stack->top != NULL) {
        struct Node* temp = stack->top;
        stack->top = stack->top->next;
        free(temp);
    }
    
    free(stack);
}

EXPORT int is_empty(struct Stack* stack) {
    if (stack == NULL) return 1;
    return stack->top == NULL;
}

EXPORT int push(struct Stack* stack, int value) {
    if (stack == NULL) return -1;
    
    struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
    if (newNode == NULL) return -2;
    
    newNode->data = value;
    newNode->next = stack->top;
    stack->top = newNode;
    
    return 0;
}

EXPORT int pop(struct Stack* stack, int* result) {
    if (stack == NULL || is_empty(stack)) return -1;
    
    struct Node* temp = stack->top;
    *result = temp->data;
    
    stack->top = stack->top->next;
    free(temp);
    
    return 0;
}

EXPORT int peek(struct Stack* stack, int* result) {
    if (stack == NULL || is_empty(stack)) return -1;
    
    *result = stack->top->data;
    return 0;
}

EXPORT int get_size(struct Stack* stack) {
    if (stack == NULL) return 0;
    
    int count = 0;
    struct Node* current = stack->top;
    
    while (current != NULL) {
        count++;
        current = current->next;
    }
    
    return count;
}

EXPORT int* get_all_elements(struct Stack* stack, int* size) {
    if (stack == NULL) {
        *size = 0;
        return NULL;
    }
    
    *size = get_size(stack);
    if (*size == 0) return NULL;
    
    int* elements = (int*)malloc(*size * sizeof(int));
    if (elements == NULL) return NULL;
    
    struct Node* current = stack->top;
    for (int i = 0; i < *size; i++) {
        elements[i] = current->data;
        current = current->next;
    }
    
    return elements;
}

EXPORT void free_elements(int* elements) {
    if (elements != NULL) {
        free(elements);
    }
}

EXPORT void clear_stack(struct Stack* stack) {
    if (stack == NULL) return;
    
    while (stack->top != NULL) {
        struct Node* temp = stack->top;
        stack->top = stack->top->next;
        free(temp);
    }
}