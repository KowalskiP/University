#ifndef STACKTEMPLATE_H_INCLUDED
#define STACKTEMPLATE_H_INCLUDED
#include <iostream>
#include "string.h"
// Класс исслючений для стека
class EStack
{
  private:
    char* msg;  // сообщение об ошибке
  public:
    EStack(const char* errmsg) { strcpy(msg, errmsg); }
    ~EStack() { delete msg; }
    const char* getmsg() { return msg; }
};
#define ESTACK_EMPTY "Stack is empty"
template <class T>
struct l1item
{
    T data;
    l1item<T>* next;
};

template <class T>
class stack{
    private:
    l1item<T>* head; // голова односвязного списка

  public:
    stack() { head = NULL; }                   // конструктор
    stack(const stack<T>&);                    // конструктор копирования
    ~stack() { clear(); }                      // деструктор
    bool empty() const { return head==NULL; }  // стек пуст?
    stack<T>& clear();                         // очистить стек
    stack<T>& del();                           // удалить элемент из стека
    stack<T>& push(const T& data);             // добавить элемент в стек
    T pop();                                   // извлечь элемент из стека
    const T& see() const;                      // посмотреть элемент в вершине стека
    stack<T>& operator = (const stack<T>&);    // оператор присваивания
};

template <class T>
stack<T>::stack(const stack<T>& Stack)
{
  head = NULL;
  *this = Stack;
}

// Очистка стека (удаление всех элементов)
template <class T>
stack<T>& stack<T>::clear()
{
  while(!empty()) del();
  return *this;
}

// Удаление элемента из вершины стека
template <class T>
stack<T>& stack<T>::del()
{
  if(empty()) throw(EStack(ESTACK_EMPTY));

  l1item<T>* tmp = head->next;
  delete head;
  head = tmp;
  return *this;
}

// Добавление элемента с стек
template <class T>
stack<T>& stack<T>::push(const T& data)
{
  l1item<T>* item = new l1item<T>;
  item->data = data;
  item->next = head;
  head = item;
  return *this;
}

// Извлечение элемента из стека
template <class T>
T stack<T>::pop()
{
  if(empty()) throw (EStack(ESTACK_EMPTY));

  l1item<T>* old = head;
  head = head->next;
  T data = old->data;
  delete old;
  return data;
}

// Просмотр элемента в вершине стека
template <class T>
const T& stack<T>::see() const
{
  if(empty()) throw (EStack(ESTACK_EMPTY));
  return head->data;
}

// Оператор присваивания
template <class T>
stack<T>& stack<T>::operator = (const stack<T>& Stack)
{
  if (this == &Stack) return *this;
  clear();
  if(!Stack.empty())
  {
    head = new l1item<T>;
    l1item<T>* cur = head;
    l1item<T>* src = Stack.head;
    while(src)
    {
      cur->data = src->data;
      if(src->next)
      {
        cur->next = new l1item<T>;
        cur = cur->next;
      } else
        cur->next = NULL;
      src = src->next;
    }
  }
  return *this;
}
#endif // STACKTEMPLATE_H_INCLUDED
