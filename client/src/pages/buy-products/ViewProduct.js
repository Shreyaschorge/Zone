import { useParams } from 'react-router-dom';

export const ViewProduct = () => {
  const { productId } = useParams();

  return <h1>View Product {productId}</h1>;
};
