import React from "react";
import { Redirect, Route } from "react-router-dom";
import Token from './utils/manageToken'

export const SecureRoute = ({component: Component, ...rest}) => {

  const auth = Token.getUser()
  
  return (
    <Route 
      {...rest}
      render={props => !auth ? <Redirect to="/auth"/> : <Component {...props} />}
    />
  )
}
