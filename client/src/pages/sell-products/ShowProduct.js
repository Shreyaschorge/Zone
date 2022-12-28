import {useParams} from 'react-router-dom'

export const ShowProduct = () => {
    const {productId} = useParams()
    return <h1>Show Product {productId}</h1>
}