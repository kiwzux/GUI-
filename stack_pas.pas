{$mode objfpc}{$H+}

library stack_pas;

uses
  SysUtils;

type
  PNode = ^TNode;
  TNode = record
    Data: Integer;
    Next: PNode;
  end;

  PStack = ^TStack;
  TStack = record
    Top: PNode;
  end;

// Экспортируемые функции
function create_stack: Pointer; cdecl; export;
procedure delete_stack(stack: Pointer); cdecl; export;
function is_empty(stack: Pointer): LongInt; cdecl; export;
function push(stack: Pointer; value: Integer): LongInt; cdecl; export;
function pop(stack: Pointer; var result: Integer): LongInt; cdecl; export;
function peek(stack: Pointer; var result: Integer): LongInt; cdecl; export;
function get_size(stack: Pointer): LongInt; cdecl; export;
function get_all_elements(stack: Pointer; var size: LongInt): Pointer; cdecl; export;
procedure free_elements(elements: Pointer); cdecl; export;
procedure clear_stack(stack: Pointer); cdecl; export;

// Реализация
function create_stack: Pointer;
var
  stack: PStack;
begin
  GetMem(stack, SizeOf(TStack));
  if Assigned(stack) then
    stack^.Top := nil;
  Result := stack;
end;

procedure delete_stack(stack: Pointer);
var
  temp: PNode;
begin
  if not Assigned(stack) then Exit;
  while Assigned((PStack(stack)).Top) do
  begin
    temp := (PStack(stack)).Top;
    (PStack(stack)).Top := temp^.Next;
    Dispose(temp);
  end;
  FreeMem(stack);
end;

function is_empty(stack: Pointer): LongInt;
begin
  Result := LongInt(not Assigned(stack) or not Assigned((PStack(stack)).Top));
end;

function push(stack: Pointer; value: Integer): LongInt;
var
  newNode: PNode;
begin
  if not Assigned(stack) then
  begin
    Result := -1;
    Exit;
  end;
  
  New(newNode);
  if not Assigned(newNode) then
  begin
    Result := -2;
    Exit;
  end;
  
  newNode^.Data := value;
  newNode^.Next := (PStack(stack)).Top;
  (PStack(stack)).Top := newNode;
  Result := 0;
end;

function pop(stack: Pointer; var result: Integer): LongInt;
var
  temp: PNode;
begin
  if not Assigned(stack) or is_empty(stack) <> 0 then
  begin
    Result := -1;
    Exit;
  end;
  
  temp := (PStack(stack)).Top;
  result := temp^.Data;
  (PStack(stack)).Top := temp^.Next;
  Dispose(temp);
  Result := 0;
end;

function peek(stack: Pointer; var result: Integer): LongInt;
begin
  if not Assigned(stack) or is_empty(stack) <> 0 then
  begin
    Result := -1;
    Exit;
  end;
  
  result := (PStack(stack)).Top^.Data;
  Result := 0;
end;

function get_size(stack: Pointer): LongInt;
var
  current: PNode;
begin
  if not Assigned(stack) then
  begin
    Result := 0;
    Exit;
  end;
  
  Result := 0;
  current := (PStack(stack)).Top;
  while Assigned(current) do
  begin
    Inc(Result);
    current := current^.Next;
  end;
end;

function get_all_elements(stack: Pointer; var size: LongInt): Pointer;
var
  i: Integer;
  current: PNode;
  count: LongInt;
begin
  if not Assigned(stack) then
  begin
    size := 0;
    Result := nil;
    Exit;
  end;
  
  count := get_size(stack);
  if count = 0 then
  begin
    size := 0;
    Result := nil;
    Exit;
  end;
  
  Result := AllocMem(SizeOf(Integer) * count);
  size := count;
  
  current := (PStack(stack)).Top;
  for i := 0 to count - 1 do
  begin
    (PIntegerArray(Result)^)[i] := current^.Data;
    current := current^.Next;
  end;
end;

procedure free_elements(elements: Pointer);
begin
  if Assigned(elements) then
    FreeMem(elements);
end;

procedure clear_stack(stack: Pointer);
var
  temp: PNode;
begin
  if not Assigned(stack) then Exit;
  while Assigned((PStack(stack)).Top) do
  begin
    temp := (PStack(stack)).Top;
    (PStack(stack)).Top := temp^.Next;
    Dispose(temp);
  end;
end;

initialization
finalization

end.