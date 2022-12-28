import { useContext, createContext, useState } from 'react'

const AppContext = createContext({
    errors: null,
    setErrors: () => { },
    cart: null,
    setCart: () => { },
    allProducts: null,
    setAllProducts: () => { }
});

const products = [
    {
        uuid: 'product_1',
        title: 'Royal Enfield Hunter 350',
        description: 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean m',
        price: 78453.76
    },
    {
        uuid: 'product_2',
        title: 'Royal Enfield Classic 650',
        description: 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean m',
        price: 178453.76
    },
    {
        uuid: 'product_3',
        title: 'TVS Ronin',
        description: 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean m',
        price: 123453.76
    },
    {
        uuid: 'product_4',
        title: 'Kawasaki Ninja',
        description: 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean m',
        price: 833453.76
    },
    {
        uuid: 'product_5',
        title: 'Harley Davidson Iron 833',
        description: 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean m',
        price: 984953.76
    },
]

export const AppProvider = ({ children }) => {

    const [errors, setErrors] = useState(null)
    const [cart, setCart] = useState([])
    const [allProducts, setAllProducts] = useState(products)

    const value = {
        errors,
        setErrors,
        cart,
        setCart,
        allProducts,
        setAllProducts
    }

    return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
}

export const useApp = () => {
    const context = useContext(AppContext);
    if (!context) throw new Error('AppContext must be used with AppProvider!');
    return context;
};