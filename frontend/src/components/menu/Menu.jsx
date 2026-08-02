import React from 'react'
import styles from './Menu.module.css';
import { Link } from 'react-router-dom';


const Menu = () => {
  return (
    <>
        <aside className={styles.sidebar}>
            <div className={styles.logo}>
                <img src="/public/Logo_colapsed.svg" alt="Logo do sistema" />
                <img src="/public/Logo_text.svg" alt="Logo do sistema" />

            </div>

            <nav className={styles.sidebar_nav}>
                <ul className={styles.menu}>
                    <li className={styles.menu_item}>
                        <Link to={'/dashboard'} className={`${styles.menu_link} ${styles.active}`}>
                            <img className={styles.icon} src="/public/ActiveDashboard_icon.svg" alt="" />
                            <span className={styles.menu_text}>Dashboard</span>
                        </Link>
                    </li>
                    <li className={styles.menu_item}>
                        <Link to={'/properties'} className={styles.menu_link}>
                            <img className={styles.icon} src="/public/Properties_icon.svg" alt="" />
                            <span className={styles.menu_text}>Imóveis</span>
                        </Link>
                    </li>
                    <li className={styles.menu_item}>
                        <Link to={'/leads'} className={styles.menu_link}>
                            <img className={styles.icon} src="/public/Leads_icon.svg" alt="" />
                            <span className={styles.menu_text}>Leads</span>
                        </Link>
                    </li>
                    <li className={styles.menu_item}>
                        <Link to={'/clients'} className={styles.menu_link}>
                            <img className={styles.icon} src="/public/Clients_icon.svg" alt="" />
                            <span className={styles.menu_text}>Clientes</span>
                        </Link>
                    </li>
                    <li className={styles.menu_item}>
                        <Link to={'/property-owners'} className={styles.menu_link}>
                            <img className={styles.icon} src="/public/Owners_icon.svg" alt="" />
                            <span className={styles.menu_text}>Proprietários</span>
                        </Link>
                    </li>
                    <li className={styles.menu_item}>
                        <Link to={'/tenant-users'} className={styles.menu_link}>
                            <img className={styles.icon} src="/public/Users_icon.svg" alt="" />
                            <span className={styles.menu_text}>Colaboradores</span>
                        </Link>
                    </li>
                    
                </ul>
            </nav>
        </aside>
        <div className={styles.bgFilter}></div>
    </>


  )
}

export default Menu