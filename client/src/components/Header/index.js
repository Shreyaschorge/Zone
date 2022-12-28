import './index.css'

export const Header = ({ title, children, ...rest }) => {
    return <div {...rest} className='container'>
        <p className={'title'}>{title}</p>
        {children}
    </div>
}