import React, { useState } from 'react';

import Menu from '../components/menu/Menu';
import AppHeader from '../components/appHeader/AppHeader';
import styles from './Settings.module.css';

const UploadIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
    <polyline points="17 8 12 3 7 8" />
    <line x1="12" y1="3" x2="12" y2="15" />
  </svg>
);

const CheckIcon = () => (
  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="20 6 9 17 4 12" />
  </svg>
);

const EyeIcon = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
    <circle cx="12" cy="12" r="3" />
  </svg>
);

const Settings = ({ onLogout }) => {
  const [activeMenu, setActiveMenu] = useState('vitrine');
  const [darkMode, setDarkMode] = useState(false);
  const [contactForm, setContactForm] = useState(true);
  const [appliedTemplate, setAppliedTemplate] = useState('padrao');
  const [selectedTemplate, setSelectedTemplate] = useState('padrao');
  const [saved, setSaved] = useState(false);

  const [colors, setColors] = useState({
    primary: '#BD0D24',
    secondary: '#FFFFFF',
    accent: '#292D30',
    text: '#494949'
  });

  const [config, setConfig] = useState({
    about: '',
    contactEmail: '',
    whatsapp: '',
    address: '',
    logo1: null,
    logo2: null
  });

  const handleColorChange = (key, value) => {
    setColors(prev => ({ ...prev, [key]: value }));
  };

  const handleConfigChange = (key, value) => {
    setConfig(prev => ({ ...prev, [key]: value }));
  };

  const handleApplyTemplate = (template) => {
    setAppliedTemplate(template);
    setSelectedTemplate(template);
  };

  const handleSave = () => {
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  const handleRevert = () => {
    setColors({
      primary: '#BD0D24',
      secondary: '#FFFFFF',
      accent: '#292D30',
      text: '#494949'
    });
    setConfig({
      about: '',
      contactEmail: '',
      whatsapp: '',
      address: '',
      logo1: null,
      logo2: null
    });
    setDarkMode(false);
    setContactForm(true);
    setAppliedTemplate('padrao');
    setSelectedTemplate('padrao');
  };

  return (
    <div>
      <Menu />
      <main style={{ marginLeft: '80px', width: 'calc(100% - 80px)', height: '100vh', overflow: 'hidden', display: 'flex', flexDirection: 'column' }}>
        <AppHeader title="Configurações da imobiliária" onLogout={onLogout} />

        <div className={styles.page}>
          <div className={styles.layout}>

            {/* ========== LEFT SIDEBAR MENU ========== */}
            <aside className={styles.settingsMenu}>
              <button
                className={`${styles.menuItem} ${activeMenu === 'vitrine' ? styles.menuItemActive : ''}`}
                onClick={() => setActiveMenu('vitrine')}
              >
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <rect x="2" y="3" width="20" height="14" rx="2" ry="2" />
                  <line x1="8" y1="21" x2="16" y2="21" />
                  <line x1="12" y1="17" x2="12" y2="21" />
                </svg>
                Vitrine Automática
              </button>
              <button
                className={`${styles.menuItem} ${activeMenu === 'assinatura' ? styles.menuItemActive : ''}`}
                onClick={() => setActiveMenu('assinatura')}
              >
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                  <polyline points="14 2 14 8 20 8" />
                  <line x1="16" y1="13" x2="8" y2="13" />
                  <line x1="16" y1="17" x2="8" y2="17" />
                </svg>
                Assinatura
              </button>
            </aside>

            {/* ========== MAIN CONTENT ========== */}
            <div className={styles.content}>

              {activeMenu === 'vitrine' ? (
                <>
                  {/* ========== LEFT COLUMN ========== */}
                  <section className={styles.column}>
                    <h2 className={styles.columnTitle}>Conteúdo da Vitrine</h2>

                    {/* Logo */}
                    <div className={styles.logoRow}>
                      <div className={styles.uploadBox}>
                        <div className={styles.uploadPlaceholder}>
                          <UploadIcon />
                        </div>
                        <p className={styles.uploadLabel}>Logo</p>
                      </div>
                      <div className={styles.uploadBox}>
                        <div className={styles.uploadPlaceholder}>
                          <UploadIcon />
                        </div>
                        <p className={styles.uploadLabel}>Logo</p>
                      </div>
                    </div>

                    {/* Sobre nós */}
                    <div className={styles.field}>
                      <label className={styles.label}>Sobre nós</label>
                      <textarea
                        className={styles.textarea}
                        value={config.about}
                        onChange={(e) => handleConfigChange('about', e.target.value)}
                        placeholder="Descreva sua imobiliária..."
                      />
                    </div>

                    {/* Formulário de contato */}
                    <div className={styles.checkboxRow}>
                      <label className={styles.checkboxLabel}>
                        <div
                          className={`${styles.checkbox} ${contactForm ? styles.checkboxChecked : ''}`}
                          onClick={() => setContactForm(!contactForm)}
                        >
                          {contactForm && <CheckIcon />}
                        </div>
                        Formulário de contato
                      </label>
                    </div>

                    {/* Email */}
                    <div className={styles.field}>
                      <label className={styles.label}>Email de contato</label>
                      <input
                        type="email"
                        className={`${styles.input} ${!contactForm ? styles.inputDisabled : ''}`}
                        value={config.contactEmail}
                        onChange={(e) => handleConfigChange('contactEmail', e.target.value)}
                        placeholder="contato@imobiliaria.com"
                        disabled={!contactForm}
                      />
                    </div>

                    {/* WhatsApp */}
                    <div className={styles.field}>
                      <label className={styles.label}>Número de WhatsApp</label>
                      <input
                        type="tel"
                        className={styles.input}
                        value={config.whatsapp}
                        onChange={(e) => handleConfigChange('whatsapp', e.target.value)}
                        placeholder="+55 13 99999-9999"
                      />
                    </div>

                    {/* Endereço */}
                    <div className={styles.field}>
                      <label className={styles.label}>Endereço físico</label>
                      <input
                        type="text"
                        className={styles.input}
                        value={config.address}
                        onChange={(e) => handleConfigChange('address', e.target.value)}
                        placeholder="Rua Exemplo, 123 - Centro"
                      />
                    </div>
                  </section>

                  {/* ========== RIGHT COLUMN ========== */}
                  <section className={styles.column}>
                    <h2 className={styles.columnTitle}>Personalização da Vitrine</h2>

                    {/* Color pickers */}
                    <div className={styles.colorsGrid}>
                      <div className={styles.colorItem}>
                        <span className={styles.colorLabel}>Cor Primária</span>
                        <div className={styles.colorPicker}>
                          <input
                            type="color"
                            className={styles.colorInputColor}
                            value={colors.primary}
                            onChange={(e) => handleColorChange('primary', e.target.value)}
                          />
                          <input
                            type="text"
                            className={styles.colorInput}
                            value={colors.primary}
                            onChange={(e) => handleColorChange('primary', e.target.value)}
                          />
                        </div>
                      </div>
                      <div className={styles.colorItem}>
                        <span className={styles.colorLabel}>Cor Auxiliar</span>
                        <div className={styles.colorPicker}>
                          <input
                            type="color"
                            className={styles.colorInputColor}
                            value={colors.secondary}
                            onChange={(e) => handleColorChange('secondary', e.target.value)}
                          />
                          <input
                            type="text"
                            className={styles.colorInput}
                            value={colors.secondary}
                            onChange={(e) => handleColorChange('secondary', e.target.value)}
                          />
                        </div>
                      </div>
                      <div className={styles.colorItem}>
                        <span className={styles.colorLabel}>Cor Secundária</span>
                        <div className={styles.colorPicker}>
                          <input
                            type="color"
                            className={styles.colorInputColor}
                            value={colors.accent}
                            onChange={(e) => handleColorChange('accent', e.target.value)}
                          />
                          <input
                            type="text"
                            className={styles.colorInput}
                            value={colors.accent}
                            onChange={(e) => handleColorChange('accent', e.target.value)}
                          />
                        </div>
                      </div>
                      <div className={styles.colorItem}>
                        <span className={styles.colorLabel}>Cor do Texto</span>
                        <div className={styles.colorPicker}>
                          <input
                            type="color"
                            className={styles.colorInputColor}
                            value={colors.text}
                            onChange={(e) => handleColorChange('text', e.target.value)}
                          />
                          <input
                            type="text"
                            className={styles.colorInput}
                            value={colors.text}
                            onChange={(e) => handleColorChange('text', e.target.value)}
                          />
                        </div>
                      </div>
                    </div>

                    {/* Preview das cores */}
                    <div className={styles.colorPreviewBox}>
                      <div className={styles.previewHeader} style={{ backgroundColor: colors.primary }}>
                        <span style={{ color: colors.secondary }}>Preview da Vitrine</span>
                      </div>
                      <div className={styles.previewBody} style={{ backgroundColor: colors.secondary }}>
                        <div className={styles.previewCard} style={{ backgroundColor: colors.accent }}>
                          <span style={{ color: colors.text }}>Imóvel</span>
                        </div>
                        <div className={styles.previewCard} style={{ backgroundColor: colors.accent }}>
                          <span style={{ color: colors.text }}>Imóvel</span>
                        </div>
                      </div>
                    </div>

                    {/* Modo escuro */}
                    <div className={styles.checkboxRow}>
                      <label className={styles.checkboxLabel}>
                        <div
                          className={`${styles.checkbox} ${darkMode ? styles.checkboxChecked : ''}`}
                          onClick={() => setDarkMode(!darkMode)}
                        >
                          {darkMode && <CheckIcon />}
                        </div>
                        Modo escuro
                      </label>
                    </div>

                    {/* Templates */}
                    <div className={styles.templatesSection}>
                      <h3 className={styles.templatesTitle}>Templates</h3>

                      <div
                        className={`${styles.templateCard} ${selectedTemplate === 'padrao' ? styles.templateSelected : ''} ${appliedTemplate === 'padrao' ? styles.templateApplied : ''}`}
                        onClick={() => setSelectedTemplate('padrao')}
                      >
                        <div className={styles.templatePreview}>
                          <div className={styles.templateMock}>
                            <div className={styles.mockHeader} />
                            <div className={styles.mockBody}>
                              <div className={styles.mockCard} />
                              <div className={styles.mockCard} />
                              <div className={styles.mockCard} />
                            </div>
                          </div>
                        </div>
                        <div className={styles.templateInfo}>
                          <div className={styles.templateNameRow}>
                            <span className={styles.templateName}>Template Padrão</span>
                            {appliedTemplate === 'padrao' && <span className={styles.appliedBadge}>Aplicado</span>}
                          </div>
                          <div className={styles.templateActions}>
                            <button className={styles.previewBtn}>
                              <EyeIcon /> Pré-visualizar
                            </button>
                            <button
                              className={`${styles.applyBtn} ${appliedTemplate === 'padrao' ? styles.applyBtnActive : ''}`}
                              onClick={(e) => { e.stopPropagation(); handleApplyTemplate('padrao'); }}
                            >
                              Aplicar
                            </button>
                          </div>
                        </div>
                      </div>

                      <div
                        className={`${styles.templateCard} ${selectedTemplate === 'classico' ? styles.templateSelected : ''} ${appliedTemplate === 'classico' ? styles.templateApplied : ''}`}
                        onClick={() => setSelectedTemplate('classico')}
                      >
                        <div className={styles.templatePreview}>
                          <div className={styles.templateMock}>
                            <div className={styles.mockHeader} />
                            <div className={styles.mockBody}>
                              <div className={styles.mockCard} />
                              <div className={styles.mockCard} />
                            </div>
                          </div>
                        </div>
                        <div className={styles.templateInfo}>
                          <div className={styles.templateNameRow}>
                            <span className={styles.templateName}>Template Clássico</span>
                            {appliedTemplate === 'classico' && <span className={styles.appliedBadge}>Aplicado</span>}
                          </div>
                          <div className={styles.templateActions}>
                            <button className={styles.previewBtn}>
                              <EyeIcon /> Pré-visualizar
                            </button>
                            <button
                              className={`${styles.applyBtn} ${appliedTemplate === 'classico' ? styles.applyBtnActive : ''}`}
                              onClick={(e) => { e.stopPropagation(); handleApplyTemplate('classico'); }}
                            >
                              Aplicar
                            </button>
                          </div>
                        </div>
                      </div>

                      <div
                        className={`${styles.templateCard} ${selectedTemplate === 'moderno' ? styles.templateSelected : ''} ${appliedTemplate === 'moderno' ? styles.templateApplied : ''}`}
                        onClick={() => setSelectedTemplate('moderno')}
                      >
                        <div className={styles.templatePreview}>
                          <div className={styles.templateMock}>
                            <div className={styles.mockHeader} />
                            <div className={styles.mockBody}>
                              <div className={styles.mockCard} />
                              <div className={styles.mockCard} />
                              <div className={styles.mockCard} />
                              <div className={styles.mockCard} />
                            </div>
                          </div>
                        </div>
                        <div className={styles.templateInfo}>
                          <div className={styles.templateNameRow}>
                            <span className={styles.templateName}>Template Moderno</span>
                            {appliedTemplate === 'moderno' && <span className={styles.appliedBadge}>Aplicado</span>}
                          </div>
                          <div className={styles.templateActions}>
                            <button className={styles.previewBtn}>
                              <EyeIcon /> Pré-visualizar
                            </button>
                            <button
                              className={`${styles.applyBtn} ${appliedTemplate === 'moderno' ? styles.applyBtnActive : ''}`}
                              onClick={(e) => { e.stopPropagation(); handleApplyTemplate('moderno'); }}
                            >
                              Aplicar
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </section>
                </>
              ) : (
                /* ========== ASSINATURA CONTENT ========== */
                <section className={styles.columnFull}>
                  <h2 className={styles.columnTitle}>Gerenciar Assinatura</h2>

                  <div className={styles.subscriptionCard}>
                    <div className={styles.subscriptionHeader}>
                      <div>
                        <h3 className={styles.planName}>Plano Profissional</h3>
                        <p className={styles.planPrice}>R$ 149,90<span className={styles.planPeriod}>/mês</span></p>
                      </div>
                      <span className={styles.planBadge}>Ativo</span>
                    </div>

                    <div className={styles.subscriptionFeatures}>
                      <div className={styles.featureItem}>
                        <CheckIcon /> Vitrine Automática
                      </div>
                      <div className={styles.featureItem}>
                        <CheckIcon /> até 50 imóveis
                      </div>
                      <div className={styles.featureItem}>
                        <CheckIcon /> Suporte prioritário
                      </div>
                      <div className={styles.featureItem}>
                        <CheckIcon /> Relatórios avançados
                      </div>
                    </div>

                    <div className={styles.subscriptionActions}>
                      <button className={styles.revertBtn}>Cancelar Assinatura</button>
                      <button className={styles.saveBtn}>Alterar Plano</button>
                    </div>
                  </div>
                </section>
              )}
            </div>
          </div>

          {/* ========== BOTTOM ACTION BAR ========== */}
          {activeMenu === 'vitrine' && (
            <div className={styles.actionBar}>
              <button className={styles.revertBtn} onClick={handleRevert}>Reverter</button>
              <button
                className={`${styles.saveBtn} ${saved ? styles.saveBtnSaved : ''}`}
                onClick={handleSave}
              >
                {saved ? '✓ Salvo!' : 'Salvar Alterações'}
              </button>
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default Settings;
