enum BidOrAsk{
    Bid,
    Ask,
}

struct Order{
    size : f64,
    bid_or_ask : BidOrAsk

}

struct Price{
    integral : u64,
    fractional : u64,
    scalar : u64,
}

impl Price{
    fn new(price: f64) -> Price{
        let scalar = 1000;
        let integral = price as u64 
        Price{
            integral = ,
            fractional = ,
            scalar = ,
        }
    }
}

struct Limit{
    price: Price,
    orders: Vec<Order>
}

impl Order{
    fn new(bid_or_ask:BidOrAsk, size:f64) -> Order{
        Order{
            bid_or_ask,size
        }
    }
}

fn main() {
    println!("Hello, world!");
}
