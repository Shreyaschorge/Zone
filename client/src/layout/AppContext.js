import { useContext, createContext, useState } from 'react'

const AppContext = createContext({
    errors: null,
    setErrors: () => { }
});

export const AppProvider = ({ children }) => {

    const [errors, setErrors] = useState(null)

    const value = {
        errors,
        setErrors
    }

    return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
}

export const useApp = () => {
    const context = useContext(AppContext);
    if (!context) throw new Error('AppContext must be used with AppProvider!');
    return context;
};