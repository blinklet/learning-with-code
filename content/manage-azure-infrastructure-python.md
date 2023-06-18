title: Manage Azure Infrastructure with Python
slug: manage-azure-infrastructure-python
summary: I wrote a new Python script that helps me manage my Azure VMs.  In this post, I share what I learned about the Azure Python SDK, Azure authorization, and sorting nested lists by key.
date: 2021-02-02
modified: 2021-02-02
category: Python
status: published

I wrote a new Python script called *azruntime*. It helps me manage my Azure VMs. The script is open-source and should work for anyone who also uses the Azure CLI. *azruntime* is available on my [azure-scripts GitHub repository](https://github.com/blinklet/azure-scripts).

![splash image showing app in screens]({static}images/manage-azure-infrastructure-python/azruntime01.png)


I learned a lot about the Azure Python SDK while working on the *azruntime* project. In this post, I share what I learned and highlight the more interesting topics like how to find information faster in the Azure Python SDK documentation, Azure authorization, and sorting nested lists by key.

<!--more-->

## Learning the Azure Python SDK and API

Microsoft offers excellent documentation of all its Azure services, including [detailed documentation for the Azure Python SDK](https://docs.microsoft.com/en-us/azure/developer/python/azure-sdk-overview). The problem may be that there is so much documentation it is hard to know where to start.

In my opinion, the best place to start is to look at the Azure sample scripts available at the following URL:

* [https://docs.microsoft.com/en-ca/samples/browse/](https://docs.microsoft.com/en-ca/samples/browse/)

Search by keyword or category. When you find a script that appears to display some of the functionality you want to implement, use a search engine to search for the Azure Python SDK classes and functions you see used in the sample scripts.

This is a faster way to find the information you need about the Azure Python SDK.

## Azure authentication for Python scripts

Azure's documentation assumes you are writing apps that run on servers and need to [authenticate](https://docs.microsoft.com/en-us/azure/developer/python/azure-sdk-authenticate?tabs=cmd) using their own [managed identity](https://docs.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/) and permissions. The examples you find when you are searching the documentation will usually describe complex scenarios. If you are writing scripts that just augment what you can do with Azure CLI, you can use a simpler authentication method: CLI-based authentication.

### Use CLI-based authentication

[Azure CLI-based authentication](https://docs.microsoft.com/en-us/azure/developer/python/azure-sdk-authenticate?tabs=cmd#cli-based-authentication-development-purposes-only) is easier to use than [creating a user-assigned managed identity](https://docs.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/how-to-manage-ua-identity-portal) and then giving it permissions to read information about each individual resource I manage. After I run the `az login` command to login to Azure CLI, any scripts I run that use CLI-based authentication will operate with my roles and permissions. 

CLI-based authentication is suitable for use in simple fact-finding scripts that help Azure users manage resources in their subscriptions. Use CLI-based authentication when you write scripts that automate operations you might normally perform with Azure CLI. My [azruntime script](https://github.com/blinklet/azure-scripts/tree/main/azruntime) is one such script.

### Risks

Microsoft recommends that CLI-based authentication be used only for development. Using CLI-based authentication can be dangerous if you have write access to Azure resources because the script runs with the same authorizations as your user account. Different users may have different roles and permissions in Azure so a script that uses CLI-based authentication might work differently, or not at all, for other users.

To mitigate these risks, I use CLI-based authentication in my production scripts where the scripts meet all of the following criteria:

* I wrote the script yourself or, if using a script someone else wrote, I have read the source code and understood it.
* Users need to manage only the infrastructure or other resources to which they personally have access. 
* The script performs read actions, only.

### Azure Identity Classes

Use either the *DefaultAzureCredential* or *AzureCliCredential* class from the [Azure Identity client library](https://docs.microsoft.com/en-us/python/api/overview/azure/identity-readme?view=azure-python) to implement CLI-based authentication in a Python script.

I do not use the [*DefaultAzureCredential* class](https://docs.microsoft.com/en-us/python/api/overview/azure/identity-readme?view=azure-python#defaultazurecredential) because it raises a lot of errors as it searches for Azure authentication credentials on the system upon which it is installed. It works, but its output is messy. It also requires you install additional dependencies, like the [PyGObject](https://pygobject.readthedocs.io/en/latest/) library, on your system.

I think it is clearer to just use the [*AzureCliCredential* class](https://azuresdkdocs.blob.core.windows.net/$web/python/azure-identity/1.4.0/azure.identity.html#azure.identity.AzureCliCredential). It is simpler to implement and it does not raise any error messages, as long as the user is logged into Azure CLI.

### Implement CLI-based authentication

In the examples below, I show how authentication and authorization work for Azure Python applications.

First, login to Azure CLI.

```
$ az login
```

As always, set up a virtual environment for development. This protects you from package conflicts that may occur with the Azure CLI packages installed on your system.

```
$ mkdir azruntime
$ cd azruntime
$ python3 -m venv env
$ source env/bin/activate
(env) $ pip install wheel
(env) $
```

Next, install the Azure Identity library:

```
(env) $ pip install azure-identity
```

To test your script's authorization code, you need to perform actions on Azure resources or services. According to the Azure Python SDK documentation, the [*azure.mgmt.resource* library module](https://docs.microsoft.com/en-us/python/api/azure-mgmt-resource/azure.mgmt.resource?view=azure-python) contains the classes that manage subscriptions and resource groups: *SubscriptionClient* and *ResourceManagementClient*. See the [Azure Python Management sample code](https://github.com/Azure-Samples/azure-samples-python-management/tree/master/samples/resources) for ideas about how to search for and manage resources.

```
(env) $ pip install azure-mgmt-resource
```

Write a simple script that gets your Azure subscription information. 

For example, I have two subscriptions and I want to write a script that prints the subscription information. Use the Python interactive prompt and the following code:

```
(env) $ python
>>> from azure.identity import AzureCliCredential
>>> from azure.mgmt.resource import SubscriptionClient
>>> cred = AzureCliCredential()
```

At this point, *cred* is an instance of the AzureCliCredential() class that contains the authentication token also used by Azure CLI. To work with subscription information, we pass the credential to the SubscriptionClient class.

```
>>> sub_client = SubscriptionClient(cred)
```

*sub_client* is an instance of the [SubscriptionClient class](https://docs.microsoft.com/en-us/python/api/azure-mgmt-resource/azure.mgmt.resource.subscriptions.subscriptionclient?view=azure-python) and it represents a connection to the subscriptions that you have permission to use in Azure. 

> **NOTE:** If you forgot to login to Azure CLI, you still would have gotten this far without any errors because the Azure Python SDK does not try to authorize an action until you actually use the resource client. 

Try printing the list of subscriptions:

```
>>> print(sub_client.subscriptions.list())
<iterator object azure.core.paging.ItemPaged at 0x7fe3298a1ee0>
```

The sub_client object queries Azure for your subscription information. This request is authorized or rejected based on the permissions assigned to the user's Azure CLI user id.

We see that the sub_client object returns an iterable. This type of object cannot be indexed so you cannot get just one item by index. You need to iterate through it to see each subscription, or you may unpack it as arguments in a function. For example:

Pull out data from the itereable using a list comprehension, as shown below.

```
>>> [[sub.display_name, sub.subscription_id] for sub in sub_client.subscriptions.list()]
[['BL-Dev','fd5a54e1-e6d6-94a1-9e02-112ec20d499e'],['BL-Prod','97dd7d07-ec4e-ed45-454a-1e629f6d5691']]
```

Or, create a generator that iterates through the set of subscriptions in another way. (This is an excuse to write my first Python generator expression!)

```
>>> subs = ([sub.display_name, sub.subscription_id] for sub in sub_client.subscriptions.list())
>>> type(subs)
<class 'generator'>
>>> next(subs)
['BL-Dev', 'fd5a54e1-e6d6-94a1-9e02-112ec20d499e']
>>> next(subs)
['BL-Prod', '97dd7d07-ec4e-ed45-454a-1e629f6d5691']
>>> next(subs)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
```

Or, dump all subscription information by unpacking the iterable as arguments to a print function.

```
>>> print(*sub_client.subscriptions.list())
{'additional_properties': {}, 'id': '/subscriptions/fd5a54e1-e6d6-94a1-9e02-112ec20d499e', 'subscription_id': 'fd5a54e1-e6d6-94a1-9e02-112ec20d499e', 'display_name': 'BL-Dev', 'tenant_id': '9d991563-8576-3e6a-09bc-90f49f943111', 'state': 'Enabled', 'subscription_policies': <azure.mgmt.resource.subscriptions.v2019_11_01.models._models_py3.SubscriptionPolicies object at 0x7fe3297ff040>, 'authorization_source': 'RoleBased', 'managed_by_tenants': [<azure.mgmt.resource.subscriptions.v2019_11_01.models._models_py3.ManagedByTenant object at 0x7fe3297ff130>], 'tags': None} {'additional_properties': {}, 'id': '/subscriptions/97dd7d07-ec4e-ed45-454a-1e629f6d5691', 'subscription_id': '97dd7d07-ec4e-ed45-454a-1e629f6d5691', 'display_name': 'BL-Prod', 'tenant_id': '9d991563-8576-3e6a-09bc-90f49f943111', 'state': 'Enabled', 'subscription_policies': <azure.mgmt.resource.subscriptions.v2019_11_01.models._models_py3.SubscriptionPolicies object at 0x7fe3297ff0d0>, 'authorization_source': 'RoleBased', 'managed_by_tenants': [], 'tags': None}
```

Quit the interactive Python prompt:

```
>>> quit()
(env) $
```

Next, use the *ResourceManagementClient* class to list all resource groups in a subscription.

Things are getting more complex so open a text editor and create a Python program that lists all resource groups in your subscriptions. It should look similar to the one shown below:

```
from azure.identity import AzureCliCredential
from azure.mgmt.resource import SubscriptionClient
from azure.mgmt.resource import ResourceManagementClient

cred = AzureCliCredential()
sub_client = SubscriptionClient(cred)
for sub in sub_client.subscriptions.list():
    sub_id = sub.subscription_id
    sub_name = sub.display_name
    resource_client = ResourceManagementClient(cred, sub_id)
    for group in resource_client.resource_groups.list():
        print(sub_name, group.name)
```

Save the file as *test1.py* and run it. You should see output similar to below:

```
(env) $ python test1.py
BL-Dev vpn2021
BL-Dev routerlab
BL-Dev labtest
BL-Dev optical
BL-Dev vpnsec
BL-Prod lab02
BL-Prod lab01
BL-Prod app-frontend
BL-Prod app-backend
BL-Prod applab  
```

You can imagine how you could keep expanding this script to list all VMs in each resource group in each subscription, get the activity logs for each VM, and so on. That's how I built my *azruntime* script.

To manage other resources in Azure, you can use other libraries. To experiment with this, install the following libraries:

```
(env) $ pip install azure-mgmt-resource
(env) $ pip install azure-mgmt-compute
(env) $ pip install azure-mgmt-monitor
```

## Sorting lists of lists by key

my *azruntime* script builds a table containing Azure VM information. Each row contains information about each VM. Each column is a specific piece of data like VM name, subscription name, location, or running time. 

In memory, I represent this table as a list of nested lists. Each nested list is a row in the table.

### Sort by key using the *itemgetter* function

The way most people sort a list of lists is to use the *key* keyword argument in either the *sorted* function or in the list object's *sort* method. While I was figuring out how to implement this, I learned about the [*operator.itemgetter*](https://docs.python.org/3/library/operator.html#operator.itemgetter) function, which is easier than [using lambda functions](https://stackoverflow.com/questions/13669252/what-is-key-lambda/13669294) in the [*sort()* function's *key* argument](https://docs.python.org/3/howto/sorting.html#key-functions). 

I used the *operator.itemgetter* function to pick an item by index from each nested list and use it as the sort key. 

First, import the *operator.itemgetter* function:

```
from operator import itemgetter
```

Then use the *sorted* function to return a new list, sorted by the items indexed in each nested list.

```
def sort_by_column(input_list, column_index):
    return(sorted(input_list, key=itemgetter(column_index)))
```

If I want to sort a table by the third column, I use *column_index = 2* when I call the function. For example:

```
sort_by_column(vm_table, 2)
```

The function needs to be more flexible. The table has a header row that contains column names and I want to sort by column name instead of index number. So, because I assume the first nested list is list of column names and that the *column_name* parameter will be a string with a value like "VMname", I write the update the function as follows:

```
def sort_by_column(input_list, column_name):
    header = input_list[0]
    rows = input_list[1:]
    column_index = header.index(column_name)
    rows.sort(key=itemgetter(column_index))
    rows.insert(0, header)
    return(rows)
```

To sort a list of lists named "vm_table" by the column name "Location", I call the function with the following statement:

```
sort_by_column(vm_table, 'Location')
```

### Argument packing and unpacking

I also learned about [*argument packing and unpacking*](https://treyhunner.com/2018/10/asterisks-in-python-what-they-are-and-how-to-use-them/), which enables you to write functions that accept a variable number of arguments and also lets you unpack iterables as arguments when you call a function. This is a Python feature that you may not appreciate when you first read about it [^1] but, when you need it, it is very useful.

[^1]: [From *Learning Python 5th Edition* by Mark Lutz](https://learning-python.com/about-lp5e.html), Chapter 18, pages 549-550 and 555-556))

I want to sort the table by more than one column name. For example, I want the table organized by "VMstatus", then by "Subscription", then by "VMsize". From the Python documentation, I know the *operator.itemgetter* function will return items recursively from a nested list if you give it more than one integer as a parameter. For example:

```
rows.sort(key=itemgetter(2, 4, 0)
```

The expression above will recursively sort a list of lists by the third column, then by the fifth column, then by the first column. It's an easy way to sort by multiple columns. But, how do I pass multiple arguments to the function? The solution is to use Python's argument packing and unpacking feature, using the asterix operator.

The new function looks like the following:

```
def sort_by_column(input_list, *args):
    header = input_list[0]
    rows = input_list[1:]
    column_indexes = [header.index(column) for column in args]
    rows.sort(key=itemgetter(*column_indexes))
    rows.insert(0, header)
    return(rows)
```

Using the asterix operator before the *args* argument in the function header means that any number of positional arguments may be entered and they are all collected in an iterable named *args*. Inside the function, we build a list of integers representing column indexes by iterating through *args*. Then, we unpack that list into the *operator.itemgetter* function's arguments using the asterix operator again.

I can call the function using one or more column names as parameters. It will recursively sort the nested lists by each column name, in order. For example:

```
sort_by_column(vm_table,'Subscription','Location','Vmsize')
```

This is a simple way to sort a table by multiple column names using Python.


## Conclusion

The rest of the source code for the *azruntime* script is available on my [*azure-scripts* GitHub repository](https://github.com/blinklet/azure-scripts). 

I used more Azure Python SDK classes to get activity logs for each VM in my subscriptions, did some math using the [*datetime* module](https://docs.python.org/3/library/datetime.html) to find the most recent "VM start" log and calculated the uptime of each VM. Then I created a table and pretty-print it using the [*Tabulate* package](https://github.com/astanin/python-tabulate).

