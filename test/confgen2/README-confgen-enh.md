# Confgen Enhancement Ideas by Chris


* Base class defines output serialization methods (or uses plug-in helper) to emit JSON, write to file, perform SAI API calls (event listener using streaming emitter?), etc.
* __main__ function allows driving from cmd-line for experiments
* __init__ accepts mix of kwargs, dict or json to assign params. Can use a global json for all generators or override selectively