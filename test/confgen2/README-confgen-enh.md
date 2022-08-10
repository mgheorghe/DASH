# Confgen Enhancement Ideas by Chris

* Create standardized classes inheriting from a base class with abstract methds
* Instantiating a class creates a generator with some standard method like items() to get list instances
* Standard method to get parant dict container but caller doesn't have to use it
* Standard method to provide variables used, count of items, etc.
* Base class defines output serialization methods (or uses plug-in helper) to emit JSON, write to file, f=perform SAI API calls (event listener using streaming emitter?), etc.
* __main__ function allows driving from cmd-line for experiments
* __init__ accepts mix of kwargs, dict or json to assign params. Can use a global json for all generators or override selectively