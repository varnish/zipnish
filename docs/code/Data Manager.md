Data manager comes into play after data has been Read from the shared memory log by [Reader](Reader.md)

Data manager recieves the following set of fields as argument to it's addLogItem function.

*VxId, Request Type, Tag, Data*

Log data for client / backend request is read inside `addLogItem()` function.

`addLogItem()` is a dictionary (key: value structure). Values are read in based upon tag value.

Upon encountering `tag == 'End'` logItem is send to [Log Storage](Storage.md) to be recorded.
