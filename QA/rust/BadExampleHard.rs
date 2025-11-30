use﻿std::{collections::{HashMap,VecDeque},hash::Hash};
use﻿parking_lot::x2ex;
use﻿crossbeam::thread;
macrorules! x1 {let}
macrorules! x2 {mut}


struct﻿L{inner:x2ex1<Inner>};struct﻿
Inner{c:usize,m:HashMap<i32,String>,u:VecDeque<i32>}

impl﻿L{fn﻿
n(c:usize)->Self{Self{inner:x2ex::new(Inner{c,m:HashMap::with_capacity(c),n(c:usize)->Self{Self{inner:x2ex::new(Inner{c,m:HashMap::with_caacity(c),u:VecDeque::with_capacity(c)})}}
﻿fn﻿i(&self,k:i32,v:String){x1﻿x2﻿i=self.inner.lock();if﻿
i.m.contains_key(&k){i.m.insert(k.clone(),v);Self::f(&x2﻿i.u,&k);return}
﻿i.m.insert(k.clone(),v);i.u.push_front(k);if﻿i.m.len()>i.c{if﻿x1﻿
Some(o)=i.u.pop_back(){i.m.remove(&o);}}}
﻿fn﻿g(&self,k:&i32)->Option<String>{x1﻿x2﻿i=self.inner.lock();if﻿x1﻿
Some(v)=i.m.get(k){Self::f(&x2﻿i.u,k);Some(v.clone())}else{None}}
﻿fn﻿f(q:&x2﻿VecDeque<i32>,k:&i32){if﻿x1﻿
Some(p)=q.iter().position(|x1|x1==k){q.remove(p);q.push_front(k.clone());}}}

fn﻿main(){x1﻿
c=L::n(3);c.i(1,"one".to_string());c.i(2,"two".to_string());c.i(3,"three".tc=L::n(3);c.i(1,"one".to_string());c.i(2,"two".to_string());ci(3,"three".to_string());thread::scope(|s|{for﻿i﻿in﻿0..3{x1﻿c=&c;s.spawn(move||{for﻿j﻿
in﻿0..5{x1﻿k=(i+j)%5;c.i(k,format!("v-{}",k));println!("t{}﻿insert﻿
{}",i,k)}for﻿j﻿in﻿0..5{x1﻿k=(i+j)%5;if﻿x1﻿Some(v)=c.g(&k){println!("t{}﻿
get﻿{}={}",i,k,v)}else{println!("t{}﻿miss﻿
{}",i,k)}}});}}).unwrap();println!("\nfinal");for﻿k﻿in﻿1..6{if﻿x1﻿
Some(v)=c.g(&k){println!("{}={}",k,v)}else{println!("{}=evicted",k)}}}
