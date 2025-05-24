#[derive(Debug)]
struct Price {
    integral:   u64,
    fractional: u64,
    scalar:     u64,
}

impl Price {
    fn new(price: f64) -> Price {
        let scalar: u64 = 100_000;                   // how many decimal places
        let integral      = price as u64;            // truncate to integer
        let fractional    = (price.fract() * scalar as f64) as u64;
        
        Price {
            integral,
            fractional,
            scalar,
        }
    }
}

enum BidOrAsk {
    Bid,
    Ask,
}

struct Order {
    size:      f64,
    bid_or_ask: BidOrAsk,
}

impl Order {
    fn new(bid_or_ask: BidOrAsk, size: f64) -> Order {
        Order { bid_or_ask, size }
    }
}

#[derive(Debug)]
struct Limit {
    price:  Price,
    orders: Vec<Order>,
}

impl Limit{
    fn new(price : f64)-> Limit {
        limit{
            price : Price :: new(price),
            orders : Vec :: new(),
        }
    }
}

fn main() {
    let price = Price::new(50.77);
    println!("Price broken down: {:?}", price);


    let limit = Limit::new(65.35);
    println!("Limit is ", Limit);
    println!("Hello, world!");
}
