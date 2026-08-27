import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

import Menu from '../components/menu/Menu';
import AppHeader from '../components/appHeader/AppHeader';
import styles from './Dashboard.module.css';

const EmptyState = ({ icon, title, description, actionLabel, actionHref }) => (
  <div className={styles.emptyState} role="status">
    <div className={styles.emptyStateIcon}>{icon}</div>
    <p className={styles.emptyStateTitle}>{title}</p>
    <p className={styles.emptyStateDesc}>{description}</p>
    {actionLabel && actionHref && (
      <Link to={actionHref} className={styles.emptyStateAction}>{actionLabel}</Link>
    )}
  </div>
);

const ErrorState = ({ message, onRetry }) => (
  <div className={styles.errorState} role="alert">
    <div className={styles.errorIcon}>
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <circle cx="12" cy="12" r="10" />
        <line x1="12" y1="8" x2="12" y2="12" />
        <line x1="12" y1="16" x2="12.01" y2="16" />
      </svg>
    </div>
    <p className={styles.errorMessage}>{message}</p>
    {onRetry && (
      <button className={styles.retryButton} onClick={onRetry}>Tentar novamente</button>
    )}
  </div>
);

const SkeletonPulse = ({ className }) => (
  <div className={`${styles.skeleton} ${className || ''}`} aria-hidden="true" />
);

const StatCardSkeleton = () => (
  <div className={styles.statCard}>
    <SkeletonPulse className={styles.skeletonTitle} />
    <SkeletonPulse className={styles.skeletonValue} />
    <SkeletonPulse className={styles.skeletonSubtitle} />
  </div>
);

const BarChartSkeleton = () => (
  <div className={styles.statCard}>
    <SkeletonPulse className={styles.skeletonTitle} />
    <div className={styles.barChart}>
      {[1, 2, 3, 4].map(i => (
        <div key={i} className={styles.barRow}>
          <SkeletonPulse className={styles.skeletonBarLabel} />
          <SkeletonPulse className={styles.skeletonBarTrack} />
        </div>
      ))}
    </div>
  </div>
);

const DonutSkeleton = () => (
  <div className={styles.statCard}>
    <SkeletonPulse className={styles.skeletonTitle} />
    <div className={styles.donutRow}>
      <SkeletonPulse className={styles.skeletonDonut} />
      <div className={styles.donutLegend}>
        <SkeletonPulse className={styles.skeletonLegend} />
        <SkeletonPulse className={styles.skeletonLegend} />
      </div>
    </div>
  </div>
);

const PropertyCardSkeleton = () => (
  <div className={styles.propertyCard}>
    <SkeletonPulse className={styles.skeletonImage} />
    <div className={styles.propertyInfo}>
      <SkeletonPulse className={styles.skeletonText} />
      <SkeletonPulse className={styles.skeletonTextSmall} />
    </div>
  </div>
);

const LineChartSkeleton = () => (
  <div className={styles.card}>
    <SkeletonPulse className={styles.skeletonTitle} />
    <SkeletonPulse className={styles.skeletonLineChart} />
  </div>
);

const LoadingDashboard = () => (
  <>
    <div className={styles.topRow}>
      <StatCardSkeleton />
      <BarChartSkeleton />
      <DonutSkeleton />
      <StatCardSkeleton />
    </div>
    <div className={styles.middleRow}>
      <div className={styles.card}>
        <SkeletonPulse className={styles.skeletonTitle} />
        <div className={styles.propertyGrid}>
          <PropertyCardSkeleton />
          <PropertyCardSkeleton />
        </div>
      </div>
      <LineChartSkeleton />
    </div>
    <div className={styles.bottomRow}>
      <SkeletonPulse className={styles.skeletonBottomCard} />
      <SkeletonPulse className={styles.skeletonBottomCard} />
    </div>
  </>
);

const SimpleLineChart = ({ data }) => {
  const width = 500;
  const height = 160;
  const padding = { top: 16, right: 16, bottom: 28, left: 36 };
  const chartWidth = width - padding.left - padding.right;
  const chartHeight = height - padding.top - padding.bottom;
  
  const maxVal = Math.max(...data.map(d => d.value));
  const minVal = 0;
  const range = maxVal - minVal || 1;
  
  const points = data.map((d, i) => ({
    x: padding.left + (i / (data.length - 1)) * chartWidth,
    y: padding.top + chartHeight - ((d.value - minVal) / range) * chartHeight,
  }));
  
  const pathD = points.map((p, i) => `${i === 0 ? 'M' : 'L'} ${p.x} ${p.y}`).join(' ');
  
  const gridLines = [0, 0.25, 0.5, 0.75, 1].map(pct => ({
    y: padding.top + chartHeight * (1 - pct),
    value: Math.round(minVal + range * pct),
  }));
  
  const areaPath = `${pathD} L ${points[points.length - 1].x} ${padding.top + chartHeight} L ${points[0].x} ${padding.top + chartHeight} Z`;
  
  return (
    <svg viewBox={`0 0 ${width} ${height}`} className={styles.lineChart} preserveAspectRatio="xMidYMid meet">
      <defs>
        <linearGradient id="lineGradient" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="var(--accent)" stopOpacity="0.12" />
          <stop offset="100%" stopColor="var(--accent)" stopOpacity="0.01" />
        </linearGradient>
      </defs>
      {gridLines.map((line, i) => (
        <g key={i}>
          <line
            x1={padding.left}
            y1={line.y}
            x2={width - padding.right}
            y2={line.y}
            stroke="var(--border)"
            strokeWidth="0.5"
            strokeDasharray="3,3"
          />
          <text
            x={padding.left - 6}
            y={line.y + 3}
            textAnchor="end"
            fontSize="8"
            fill="var(--text)"
            opacity="0.4"
          >
            {line.value}
          </text>
        </g>
      ))}
      <path d={areaPath} fill="url(#lineGradient)" />
      <path
        d={pathD}
        fill="none"
        stroke="var(--accent)"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      {points.map((p, i) => (
        <circle
          key={i}
          cx={p.x}
          cy={p.y}
          r="3"
          fill="var(--bg)"
          stroke="var(--accent)"
          strokeWidth="2"
        />
      ))}
      {data.map((d, i) => (
        <text
          key={i}
          x={points[i].x}
          y={height - 8}
          textAnchor="middle"
          fontSize="9"
          fill="var(--text)"
          opacity="0.6"
        >
          {d.label}
        </text>
      ))}
    </svg>
  );
};

const Dashboard = ({ onLogout }) => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [data, setData] = useState(null);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      await new Promise(resolve => setTimeout(resolve, 800));
      
      const mockData = {
        leadsWaiting: 12,
        leadsToday: 3,
        propertiesByStatus: [
          { label: 'Rascunho', value: 5 },
          { label: 'Cadastrados', value: 47 },
          { label: 'Publicados', value: 72 },
          { label: 'Fechados', value: 28 },
        ],
        distribution: { venda: 58, locacao: 42 },
        monthlyNew: 15,
        monthlyGrowth: 5,
        monthlyBreakdown: [
          { type: 'Apartamentos', count: 7 },
          { type: 'Casas', count: 5 },
          { type: 'Terrenos', count: 2 },
          { type: 'Comércio', count: 1 },
        ],
        recentProperties: [
          {
            id: 1,
            title: 'Imóvel ponta da praia',
            address: 'Av. Bartolomeu de Gusmão, 382',
            price: 'R$ 450.000',
            image: 'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=400&h=300&fit=crop',
          },
          {
            id: 2,
            title: 'Imóvel ponta da praia',
            address: 'Rua Duque de Caxias, 218',
            price: 'R$ 1.300.000',
            image: 'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=400&h=300&fit=crop',
          },
        ],
        leadsOverTime: [
          { label: 'Jan', value: 20 },
          { label: 'Fev', value: 35 },
          { label: 'Mar', value: 28 },
          { label: 'Abr', value: 45 },
          { label: 'Mai', value: 52 },
          { label: 'Jun', value: 68 },
        ],
        visitors: 300,
        visitorsGrowth: 5,
      };
      
      setData(mockData);
    } catch (err) {
      setError('Não foi possível carregar os dados. Verifique sua conexão e tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const maxBar = data ? Math.max(...data.propertiesByStatus.map(d => d.value)) : 100;

  return (
    <div>
      <Menu />
      <main style={{ marginLeft: '80px', width: 'calc(100% - 80px)' }}>
        <AppHeader title="Dashboard" onLogout={onLogout} />
        
        <div 
          className={styles.dashboard}
          aria-busy={loading}
          aria-live="polite"
          aria-label="Painel de controle"
        >
          {loading && <LoadingDashboard />}
          
          {!loading && error && (
            <ErrorState message={error} onRetry={fetchData} />
          )}
          
          {!loading && !error && data && (
            <>
              <div className={styles.topRow}>
                <div className={`${styles.statCard} ${styles.statCardAccent}`} role="region" aria-label="Leads pendentes">
                  <p className={styles.statCardTitle}>Leads Aguardando</p>
                  <div className={styles.leadsValueRow}>
                    <p className={styles.leadsBigValue}>{data.leadsWaiting}</p>
                    <div className={styles.leadsMeta}>
                      <span className={styles.statCardBadge}>+{data.leadsToday} hoje</span>
                    </div>
                  </div>
                </div>

                <div className={styles.statCard} role="region" aria-label="Imóveis por status">
                  <p className={styles.statCardTitle}>Imóveis no sistema</p>
                  <div className={styles.barChart}>
                    {data.propertiesByStatus.map((item) => (
                      <div key={item.label} className={styles.barRow}>
                        <span className={styles.barLabel}>{item.label}</span>
                        <div className={styles.barTrack}>
                          <div
                            className={styles.barFill}
                            style={{ width: `${(item.value / maxBar) * 100}%` }}
                          />
                        </div>
                        <span className={styles.barValue}>{item.value}</span>
                      </div>
                    ))}
                  </div>
                </div>

                <div className={`${styles.statCard} ${styles.donutCard}`} role="region" aria-label="Distribuição dos imóveis">
                  <p className={styles.statCardTitle}>Distribuição dos imóveis por tipo</p>
                  <div className={styles.donutRow}>
                    <div
                      className={styles.donut}
                      style={{
                        background: `conic-gradient(var(--accent) 0% ${data.distribution.venda}%, var(--border) ${data.distribution.venda}% 100%)`,
                      }}
                      role="img"
                      aria-label={`${data.distribution.venda}% venda, ${data.distribution.locacao}% locação`}
                    >
                      <div className={styles.donutCenter} />
                    </div>
                    <div className={styles.donutLegend}>
                      <div className={styles.legendItem}>
                        <span className={styles.legendDot} style={{ background: 'var(--accent)' }} />
                        <span>Venda</span>
                        <span className={styles.legendValue}>{data.distribution.venda}%</span>
                      </div>
                      <div className={styles.legendItem}>
                        <span className={styles.legendDot} style={{ background: 'var(--border)' }} />
                        <span>Locação</span>
                        <span className={styles.legendValue}>{data.distribution.locacao}%</span>
                      </div>
                    </div>
                  </div>
                </div>

                <div className={styles.statCard} role="region" aria-label="Imóveis cadastrados este mês">
                  <p className={styles.statCardTitle}>Novos este mês</p>
                  <div className={styles.monthlyHeader}>
                    <p className={styles.statCardValue}>+{data.monthlyNew}</p>
                    <span className={styles.statCardGrowth}>+{data.monthlyGrowth}%</span>
                  </div>
                  <ul className={styles.monthlyList}>
                    {data.monthlyBreakdown.map(item => (
                      <li key={item.type} className={styles.monthlyItem}>
                        <span className={styles.monthlyItemType}>{item.type}</span>
                        <span className={styles.monthlyItemCount}>{item.count}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              <div className={styles.middleRow}>
                <div className={styles.card} role="region" aria-label="Imóveis visitados recentemente">
                  <h2 className={styles.cardTitle}>Visitados recentemente</h2>
                  {data.recentProperties.length === 0 ? (
                    <EmptyState
                      icon={<svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" /><polyline points="9 22 9 12 15 12 15 22" /></svg>}
                      title="Nenhum imóvel visitado"
                      description="Ao abrir imóveis, eles aparecerão aqui."
                      actionLabel="Ver imóveis"
                      actionHref="/properties"
                    />
                  ) : (
                    <div className={styles.propertyGrid}>
                      {data.recentProperties.map((prop) => (
                        <Link key={prop.id} to={`/properties/${prop.id}`} className={styles.propertyCard}>
                          <div className={styles.propertyImageWrap}>
                            <img src={prop.image} alt={prop.title} className={styles.propertyImage} />
                          </div>
                          <div className={styles.propertyInfo}>
                            <p className={styles.propertyTitle}>{prop.title}</p>
                            <p className={styles.propertyAddress}>{prop.address}</p>
                            <p className={styles.propertyPrice}>{prop.price}</p>
                          </div>
                        </Link>
                      ))}
                    </div>
                  )}
                </div>

                <div className={styles.card} role="region" aria-label="Novos leads nos últimos meses">
                  <h2 className={styles.cardTitle}>Leads por período</h2>
                  {data.leadsOverTime.length === 0 ? (
                    <EmptyState
                      icon={<svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5"><path d="M18 20V10" /><path d="M12 20V4" /><path d="M6 20v-6" /></svg>}
                      title="Sem dados de leads"
                      description="Quando novos leads chegarem, o gráfico será exibido aqui."
                    />
                  ) : (
                    <div className={styles.chartContainer}>
                      <SimpleLineChart data={data.leadsOverTime} />
                    </div>
                  )}
                </div>
              </div>

              <div className={styles.bottomRow}>
                <div className={styles.bottomCard} role="region" aria-label="Visitantes do site">
                  <div className={styles.bottomCardContent}>
                    <span className={styles.bottomCardValue}>+{data.visitors}</span>
                    <div className={styles.bottomCardText}>
                      <span className={styles.bottomCardLabel}>Visitantes</span>
                      <span className={styles.bottomCardSub}>últimos 30 dias · +{data.visitorsGrowth}%</span>
                    </div>
                  </div>
                </div>

                <div className={styles.bottomCard} role="region" aria-label="Origem dos leads">
                  <div className={styles.bottomCardContent}>
                    <svg className={styles.bottomCardIcon} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <circle cx="12" cy="12" r="10" />
                      <line x1="2" y1="12" x2="22" y2="12" />
                      <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z" />
                    </svg>
                    <div className={styles.bottomCardText}>
                      <span className={styles.bottomCardLabel}>Leads vindo de portais</span>
                      <span className={styles.bottomCardSub}>em breve</span>
                    </div>
                  </div>
                </div>
              </div>
            </>
          )}
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
