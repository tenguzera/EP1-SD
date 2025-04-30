namespace py apache_test

struct Void {}

struct LongValue {
  1: i64 value
}

struct LongArray {
  1: list<i64> values
}

struct StringValue {
  1: string value
}

struct ComplexValue {
  1: i64 id,
  2: string name
}

service TestService {
  void voidCall(),
  LongValue longCall(1: LongValue val),
  LongValue longArrayCall(1: LongArray arr),
  StringValue stringCall(1: StringValue val),
  ComplexValue complexCall(1: ComplexValue val),
}
