import { useApp } from "../../layout/AppContext";

export const Cart = () => {
  const { cart } = useApp()
  return <h1>
    {JSON.stringify(cart)}
  </h1>;
};
