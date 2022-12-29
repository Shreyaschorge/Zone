import { useContext, createContext, useState } from 'react'

const AppContext = createContext({
    errors: [],
    setErrors: () => { },
    cart: [],
    setCart: () => { },
    allProducts: [],
    setAllProducts: () => { }
});

export const AppProvider = ({ children }) => {

    const [errors, setErrors] = useState(null)
    const [cart, setCart] = useState([])
    const [allProducts, setAllProducts] = useState([])

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