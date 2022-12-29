import { useParams } from 'react-router-dom';

export const Order = () => {
    const { orderId } = useParams();

    return <h1>Order {orderId}</h1>;
};
