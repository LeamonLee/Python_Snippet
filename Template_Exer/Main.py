from string import Template


class MyTemplate(Template):
    delimiter = '&'             # can change the another delimiter by ineriting Template
                                # and override the delimiter property.

def main():
    cart = []
    cart.append(dict(item="coke", price=10, quantity=1))
    cart.append(dict(item="cake", price=11, quantity=2))
    cart.append(dict(item="fish", price=12, quantity=3))

    tplte = Template("$quantity * $item = $price")
    myTplte = MyTemplate("&quantity * &item = &price")

    total = 0
    print("Template ->")
    for data in cart:
        print(tplte.substitute(data))
        total += data["price"]
    
    print()
    total = 0
    print("myTemplate ->")
    for data in cart:
        print(myTplte.substitute(data))
        total += data["price"]
    
    print("Total price: {}".format(total))


if __name__ == "__main__":
    main()