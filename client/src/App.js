import './App.css';
import 'antd/dist/reset.css';

import {
  Switch,
  Route,
  Redirect,
  BrowserRouter as Router
} from "react-router-dom";

import Token from './utils/manageToken';
import { Auth } from './pages/auth'
import { SecureRoute } from './secureRoute';
import { BuyProducts } from './pages/buy-products/BuyProducts';
import { ViewProduct } from './pages/buy-products/ViewProduct';
import { Cart } from './pages/buy-products/Cart';
import { Order } from './pages/buy-products/Order';
import { OrderList } from './pages/buy-products/OrderList';
import { SellProducts } from './pages/sell-products/SellProducts';
import { AddProduct } from './pages/sell-products/AddProduct';
import { ShowProduct } from './pages/sell-products/ShowProduct';
import { NotFound } from './pages/NotFound';

function App() {

  const isAuthenticated = Token.getUser()

  const getApp = () => {
    return (
      <Switch>
        <SecureRoute exact path='/'>
          <Redirect to="/buy-products" />
        </SecureRoute>
        <SecureRoute path='/buy-products' exact component={BuyProducts}/>
        <SecureRoute path='/buy-products/cart' exact component={Cart}/>
        <SecureRoute path='/buy-products/orders' exact component={OrderList}/>
        <SecureRoute path='/buy-products/orders/:orderId' exact component={Order}/>
        <SecureRoute path='/buy-products/:productId' exact component={ViewProduct}/>
        <SecureRoute path='/sell-products' exact component={SellProducts}/>
        <SecureRoute path='/sell-products/add-product' exact component={AddProduct}/>
        <SecureRoute path='/sell-products/:productId' exact component={ShowProduct}/>
        <Route path='*' component={NotFound}/>
      </Switch>
    )
  }

  const getAuthRoute = () => {
    return(
      <Switch>
        <Redirect exact from='/' to='/auth' />
        <Route path='/auth' exact component={Auth} />
        <Route path='*' component={NotFound}/>
      </Switch>
    )
  }

  return (
    <Router>
        {isAuthenticated ? getApp() : getAuthRoute()}
    </Router>
  );
}

export default App;
