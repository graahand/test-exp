# REST [REPRESENTATIONAL STATE TRANSFER] API

REST stands for representational state transfer and is a software architecture style that defines a pattern for client and server communications over a network. Performance, scalability, simplicity and reliability are some of the features of the REST architecture which ease the development of websites and software.

### Constraints

1. Stateless server that doesn’t maintain the state between requests from the client. In simpler words, it doesn’t remember anything about the past requests which keep the task of request and response simple and robust.
2. Independent server and client by decoupling each other allowing the changes and updates integration seamless, making maintenance easier.
3. The data retrieved from the server should be cacheable either by client or the server which reduces the load on server along with improved performance.
4. REST architecture may contain the intermediary layers like helpers between the client and the main server which allow the security, traffic and adding extra features. The client may access the resources on the server indirectly through other layers such as proxy or load balancer. 
5. The server will provide a uniform interface for accessing resources without defining their representation. There is a standard way to request and response task no matter what kind of data it is. Those standard includes
    1. Resources and URLs: Each individual data have their unique address.
    2. HTTP Methods: These methods includes standard methods like GET(get/read data), POST(create/order new data), PUT/PATCH(update existing data) and DELETE(remove  data). 
    3. Representations: Data is sent in standard formats like JSON or XML.

These constraints mentioned above aren’t a set of specificiation, rather a the guidelines and best practices to build a web system. The more we adhere these principles, the benefits we will get but its not strictly set to follow these rules. 

## REST APIs and Web Services

REST web service is any web service that adheres to REST architecture constraints. These web services expose their data to the outside world through an API which can be accessed using the REST API with public web URLs. 

Github’s REST API URL: `https://api.github.com/users/<username>`

The data is accessed from REST API by sending HTTP requests to specific URL, it listens to HTTP methods to know which operations to perform on the web service’s resources. Resource can be accessed and manipulated with  HTTP requests.

### Status Code

1. 2xx: Successful Operation
2. 3xx: Redirection
3. 4xx: Client Error
4. 5xx: Server Error

### API Endpoints[Door to Web Service]

REST API exposes a set of public URLS thatclient applications use to access the resources of a webn service. These URLs are called endpoints. Each endpoint is designed for a specific purpose. Endpoint URL allow to choose the web service resource that the HTTP method wants to interact with.