import styles from './showcaseLayout.module.css';

export default function ShowcaseLayout({ info, children }) {
  return (
    <div className={styles.showcase}>
      <header className={styles.header}>
        <div className={styles.headerContent}>
          <div className={styles.brand}>
            {info.logo && (
              <img src={info.logo} alt={info.name} className={styles.logo} />
            )}
            <div>
              <h1 className={styles.name}>{info.name}</h1>
              {info.slogan && <p className={styles.slogan}>{info.slogan}</p>}
            </div>
          </div>
          <nav className={styles.contact}>
            {info.phone && (
              <a href={`tel:${info.phone}`} className={styles.contactLink}>
                {info.phone}
              </a>
            )}
            {info.email && (
              <a href={`mailto:${info.email}`} className={styles.contactLink}>
                {info.email}
              </a>
            )}
          </nav>
        </div>
      </header>

      <main className={styles.main}>{children}</main>

      <footer className={styles.footer}>
        <p>&copy; {new Date().getFullYear()} {info.name}</p>
      </footer>
    </div>
  );
}
