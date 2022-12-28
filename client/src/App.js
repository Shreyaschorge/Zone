import './App.css';
import 'antd/dist/reset.css';
import { useEffect } from 'react';

import {
  Switch,
  Route,
  Redirect,
  BrowserRouter as Router,
} from 'react-router-dom';

import Token from './utils/manageToken';
import { Auth } from './pages/auth';
import { SecureRoute } from './secureRoute';
import { BuyProducts } from './pages/buy-products/BuyProducts';
import { ViewProduct } from './pages/buy-products/ViewProduct';
import { Cart } from './pages/buy-products/Cart';
import { Order } from './pages/buy-products/Order';
import { OrderList } from './pages/buy-products/OrderList';
import { SellProducts } from './pages/sell-products/SellProducts';
import { ShowProduct } from './pages/sell-products/ShowProduct';
import { NotFound } from './pages/NotFound';
import { useApp } from './layout/AppContext'
import { notification } from 'antd'
import Layout from './layout/Layout';

function App() {

  const { errors } = useApp()
  const isAuthenticated = Token.getUser();

  useEffect(() => {
    if (errors) {
      errors.forEach((error) => {
        notification.error({
          message: error.message,
          placement: "bottomRight"
        });
      })
    }
  }, [errors]);


  const getApp = () => {
    return (
      <Layout>
        <Switch>
          <SecureRoute exact path="/">
            <Redirect to="/buy-products" />
          </SecureRoute>
          <SecureRoute path="/buy-products" exact component={BuyProducts} />
          <SecureRoute path="/buy-products/cart" exact component={Cart} />
          <SecureRoute path="/buy-products/orders" exact component={OrderList} />
          <SecureRoute
            path="/buy-products/orders/:orderId"
            exact
            component={Order}
          />
          <SecureRoute
            path="/buy-products/:productId"
            exact
            component={ViewProduct}
          />
          <SecureRoute path="/sell-products" exact component={SellProducts} />
          <SecureRoute
            path="/sell-products/:productId"
            exact
            component={ShowProduct}
          />
          <Route path="*" component={NotFound} />
        </Switch>
      </Layout>
    );
  };

  const getAuthRoute = () => {
    return (
      <Switch>
        <Redirect exact from="/" to="/auth" />
        <Route path="/auth" exact component={Auth} />
        <Route path="*" component={NotFound} />
      </Switch>
    );
  };

  return <Router>{isAuthenticated ? getApp() : getAuthRoute()}</Router>;
}

export default App;
