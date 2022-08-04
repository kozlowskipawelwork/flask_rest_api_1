
#from distutils import errors
#from urllib import response
from flask import Flask, jsonify, make_response, render_template, request


app = Flask(__name__)
@app.route('/')# basic homepage
def hello_world():
    return 'Hello World'


@app.route('/test-page')# basic page
def test_page():#always make a new name for the route(?)
    return 'Hello Tester!'


@app.route('/html')# basic html page rendering
def html_page():
    return render_template('index.html')


@app.route('/query-string')# a route for querying strings
def get_query_string():
    if request.args:
        req = request.args
        return ' '.join(f'{k}:{v}' for k, v in req.items())    
    return 'no query' 


# a order collection containing order details 
order ={
    '1':{
        'Size':'Small',
        'Toppings':'Cheese',#can i assign many values to a key here? I suppose I can
        'Crust':'Thin'
    },
    '2':{
        'Size':'Medium',
        'Toppings':'Cheese',
        'Crust':'Burned'
    }
    
}

#HTTP GET method is an default one, no need to specify it
@app.route('/orders-list')
def get_orders_list():
    response = make_response(jsonify(order),200)#explain this one
    return response

#HTTP GET method that returns a key and values
@app.route("/orders-list/<order_id>")#needs to be in "" braces?
def get_order_list_orders(order_id):
    if order_id in order:
        response = make_response(jsonify(order[order_id]),200)
        return response

    return 'Order not found'

#HTTP GET method that returns a particular value from a key
@app.route("/orders-list/<order_id>/<items>")
def get_order_details(order_id,items):
    item = order[order_id].get(items)
    if item:
        response = make_response(jsonify(item),200)
        return response

    return 'Order not found'

#HTTP POST method that creates a new key and values
@app.route("/orders-list/<order_id>", methods=["POST"])
def make_order(order_id):
    req = request.get_json()
    if order_id in order:
        response = make_response(jsonify({'error':'order key already exists'}),202)
        return response
    order.update({order_id:req})
    response = make_response(jsonify({'message':'order added'}),201)
    return response

#HTTP PUT method that updates a key and values it they exist or make a new one
@app.route("/orders-list/<order_id>", methods=["PUT"])
def change_order(order_id):
    req = request.get_json()
    if order_id in order:
        order[order_id]=req
        response = make_response(jsonify({'message':'order updated'}),200)
        return response
    #order.update({order_id:req})
    order[order_id]=req
    response = make_response(jsonify({'message':'new order added by PUT'}),201)
    return response

#HTTP PATCH method that updates a single value within a key
@app.route("/orders-list/<order_id>", methods=["PATCH"])
def change_order_details(order_id):
    req = request.get_json()
    if order_id in order:
        for k,v in req.items():
            order[order_id][k]=v
        response = make_response(jsonify({'message':'order updated by patch'}),200)
        return response
    order[order_id]=req
    response = make_response(jsonify({'message':'new order added by patch'}),200)
    return response

#HTTP DELETE method that deletes a key and the values
@app.route("/orders-list/<order_id>", methods=["DELETE"])
def remove_order(order_id):
    if order_id in order:
        del order[order_id]
        response = make_response(jsonify({'message' : 'order deleted'}),204)
        return response
    response = make_response(jsonify({'error' : 'order already exists? deleted???'}),404)#clarify this
    #if errors: return (jsonify('errors'): errors
    return response

if __name__ == '__main__':
    app.run(debug=True)

    #test change
