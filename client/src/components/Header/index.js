import './index.css'

export const Header = ({ title, children }) => {
    return <div className='container'>
        <p className={'title'}>{title}</p>
        {children}
    </div>
}