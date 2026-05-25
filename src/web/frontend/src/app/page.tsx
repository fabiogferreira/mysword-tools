'use client';

import React, { useState, useEffect, useRef } from 'react';
import { translations, Language } from './translations';

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function Home() {
  const [lang, setLang] = useState<Language>('pt');
  const [file, setFile] = useState<File | null>(null);
  const [dragActive, setDragActive] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [critiqueResult, setCritiqueResult] = useState<any>(null);
  
  // Opções de conversão
  const [title, setTitle] = useState('');
  const [author, setAuthor] = useState('');
  const [abbreviation, setAbbreviation] = useState('');
  const [splitByHeading, setSplitByHeading] = useState(true);
  const [headingLevel, setHeadingLevel] = useState(1);
  
  const [converting, setConverting] = useState(false);
  const [convertedFileUrl, setConvertedFileUrl] = useState<string | null>(null);
  const [convertedFilename, setConvertedFilename] = useState('');
  const [faqOpen, setFaqOpen] = useState<number | null>(null);
  
  const fileInputRef = useRef<HTMLInputElement>(null);
  const t = translations[lang];

  // Detecta o idioma do navegador de forma segura no lado do cliente
  useEffect(() => {
    const localLang = localStorage.getItem('lang') as Language;
    if (localLang && ['en', 'es', 'pt'].includes(localLang)) {
      setLang(localLang);
    } else {
      const browserLang = navigator.language.split('-')[0];
      if (['en', 'es', 'pt'].includes(browserLang)) {
        setLang(browserLang as Language);
      }
    }
  }, []);

  const changeLanguage = (newLang: Language) => {
    setLang(newLang);
    localStorage.setItem('lang', newLang);
  };

  // Drag & Drop Handlers
  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = async (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const droppedFile = e.dataTransfer.files[0];
      if (droppedFile.name.endsWith('.docx')) {
        await processFile(droppedFile);
      } else {
        setError(lang === 'pt' ? 'Apenas arquivos .docx são permitidos.' : 'Only .docx files are allowed.');
      }
    }
  };

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      await processFile(e.target.files[0]);
    }
  };

  const triggerFileInput = () => {
    fileInputRef.current?.click();
  };

  // Envia arquivo para análise preliminar (critique) no backend
  const processFile = async (selectedFile: File) => {
    setFile(selectedFile);
    setAnalyzing(true);
    setError(null);
    setCritiqueResult(null);
    setConvertedFileUrl(null);
    
    const formData = new FormData();
    formData.append('file', selectedFile);
    
    try {
      const response = await fetch(`${API_URL}/api/critique`, {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error(lang === 'pt' ? 'Falha ao analisar o documento.' : 'Failed to analyze document.');
      }
      
      const data = await response.json();
      setCritiqueResult(data);
      
      // Pré-preenche os campos de conversão com os metadados extraídos
      setTitle(data.metadata.title || selectedFile.name.replace('.docx', ''));
      setAuthor(data.metadata.author || '');
      setAbbreviation(data.metadata.abbreviation || '');
    } catch (err: any) {
      setError(err.message || 'Error communicating with server.');
      setFile(null);
    } finally {
      setAnalyzing(false);
    }
  };

  // Realiza a conversão definitiva
  const handleConvert = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;
    
    setConverting(true);
    setError(null);
    setConvertedFileUrl(null);
    
    const formData = new FormData();
    formData.append('file', file);
    formData.append('title', title);
    formData.append('author', author);
    formData.append('abbreviation', abbreviation);
    formData.append('split_by_heading', String(splitByHeading));
    formData.append('heading_level', String(headingLevel));
    
    try {
      const response = await fetch(`${API_URL}/api/convert`, {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error(lang === 'pt' ? 'Erro na conversão.' : 'Conversion error.');
      }
      
      // Recebe o arquivo SQLite final como um blob binário
      const blob = await response.blob();
      const downloadUrl = URL.createObjectURL(blob);
      setConvertedFileUrl(downloadUrl);
      setConvertedFilename(title.replace(/\s+/g, '_') + '.jor.mybible');
    } catch (err: any) {
      setError(err.message || 'Error generating MySword database.');
    } finally {
      setConverting(false);
    }
  };

  // Redireciona para o Stripe Checkout (Sandbox)
  const handlePayment = async (plan: 'single' | 'monthly' | 'yearly') => {
    setError(null);
    try {
      const formData = new FormData();
      formData.append('plan', plan);
      formData.append('success_url', window.location.origin + '/?payment=success');
      formData.append('cancel_url', window.location.origin + '/?payment=cancel');
      
      const response = await fetch(`${API_URL}/api/checkout`, {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error('Checkout session creation failed.');
      }
      
      const data = await response.json();
      if (data.checkout_url) {
        // Redireciona o navegador do usuário
        window.location.href = data.checkout_url;
      }
    } catch (err: any) {
      setError(lang === 'pt' ? 'Erro ao conectar ao Stripe.' : 'Error connecting to Stripe.');
    }
  };

  const toggleFaq = (index: number) => {
    setFaqOpen(faqOpen === index ? null : index);
  };

  return (
    <>
      {/* Elementos de Brilho de Fundo CSS */}
      <div className="bg-glow-container">
        <div className="bg-glow-1"></div>
        <div className="bg-glow-2"></div>
      </div>

      {/* Header / Navbar */}
      <header className="navbar app-container">
        <div className="logo">
          <span className="logo-icon">📖</span>
          {t.brand}
        </div>
        <nav>
          <ul className="nav-links">
            <li><a href="#uploader">{t.nav.uploader}</a></li>
            <li><a href="#features">{t.nav.features}</a></li>
            <li><a href="#pricing">{t.nav.pricing}</a></li>
            <li><a href="#faq">{t.nav.faq}</a></li>
          </ul>
        </nav>
        <div className="controls-right">
          <select 
            className="lang-selector" 
            value={lang} 
            onChange={(e) => changeLanguage(e.target.value as Language)}
          >
            <option value="en">English (US)</option>
            <option value="es">Español</option>
            <option value="pt">Português (BR)</option>
          </select>
        </div>
      </header>

      {/* Hero Section */}
      <section className="hero app-container">
        <span className="hero-tagline">{t.hero.tagline}</span>
        <h1 className="hero-title">{t.hero.title}</h1>
        <p className="hero-subtitle">{t.hero.subtitle}</p>
        <a href="#uploader" className="btn-primary">
          <span>⚡</span> {t.hero.cta}
        </a>
      </section>

      {/* Interactive Uploader Card */}
      <section id="uploader" className="uploader-section app-container">
        <div className="uploader-card">
          <h2 className="uploader-title">{t.uploader.title}</h2>
          
          <div style={{ textAlign: 'center', marginBottom: '24px', fontSize: '14px', color: 'var(--text-muted)' }}>
            <span>📝 </span>
            {lang === 'pt' ? 'Baixe o nosso ' : lang === 'es' ? 'Descargue nuestra ' : 'Download our '}
            <a 
              href="/template_estudo_biblico.docx" 
              download 
              style={{ color: 'var(--primary-color)', textDecoration: 'underline', fontWeight: '600' }}
            >
              {lang === 'pt' ? 'Modelo de Word (.docx)' : lang === 'es' ? 'Plantilla de Word (.docx)' : 'Word Template (.docx)'}
            </a>
            {lang === 'pt' ? ' para estruturar seus estudos sem erros.' : lang === 'es' ? ' para estructurar sus estudios sin errores.' : ' to format your studies error-free.'}
          </div>
          
          {error && (
            <div className="suggestion-item error" style={{ marginBottom: '24px' }}>
              <div className="sug-header">⚠️ {error}</div>
            </div>
          )}

          {/* Área de Arrastar/Escolher arquivo */}
          {!file && !analyzing && (
            <div 
              className={`dropzone ${dragActive ? 'active' : ''}`}
              onDragEnter={handleDrag}
              onDragOver={handleDrag}
              onDragLeave={handleDrag}
              onDrop={handleDrop}
              onClick={triggerFileInput}
            >
              <div className="upload-icon">📂</div>
              <p className="upload-text">{t.uploader.dragDrop}</p>
              <button type="button" className="btn-primary" style={{ padding: '8px 18px', fontSize: '14px', marginTop: '12px' }}>
                {t.uploader.browse}
              </button>
              <input 
                type="file" 
                ref={fileInputRef}
                className="file-input" 
                accept=".docx"
                onChange={handleFileChange}
              />
              <p className="upload-subtext" style={{ marginTop: '12px' }}>
                .docx (Word Document)
              </p>
            </div>
          )}

          {/* Loader de Análise */}
          {analyzing && (
            <div className="loader-wrapper">
              <div className="spinner"></div>
              <p className="upload-text">{t.uploader.analyzing}</p>
            </div>
          )}

          {/* Resultados da Validação & Opções */}
          {file && critiqueResult && (
            <div className="critique-box">
              <div className="critique-title">
                <span>📋</span> {t.uploader.critiqueHeader}
              </div>

              {/* Lista de Sugestões e Críticas */}
              <div className="suggestions-list">
                {/* Se não tem token, avisa */}
                {!critiqueResult.has_token && (
                  <div className="suggestion-item warning">
                    <div className="sug-header">⚠️ {t.uploader.noTokenWarning}</div>
                  </div>
                )}
                
                {critiqueResult.suggestions.map((sug: any, idx: number) => (
                  <div key={idx} className={`suggestion-item ${sug.level.toLowerCase()}`}>
                    <div className="sug-header">
                      {sug.level === 'ERROR' ? '❌' : sug.level === 'WARNING' ? '⚠️' : 'ℹ️'} {sug.message}
                    </div>
                    {sug.suggestion && <div className="sug-tip">{sug.suggestion}</div>}
                  </div>
                ))}
              </div>

              {/* Formulário de Configuração e Metadados */}
              <form onSubmit={handleConvert}>
                <h3 className="critique-title" style={{ fontSize: '16px', marginTop: '24px' }}>
                  <span>⚙️</span> {t.uploader.metadata}
                </h3>
                
                <div className="metadata-grid">
                  <div className="form-group">
                    <label>{t.uploader.titleLabel}</label>
                    <input 
                      type="text" 
                      className="form-input" 
                      value={title} 
                      onChange={(e) => setTitle(e.target.value)} 
                      required 
                    />
                  </div>
                  <div className="form-group">
                    <label>{t.uploader.authorLabel}</label>
                    <input 
                      type="text" 
                      className="form-input" 
                      value={author} 
                      onChange={(e) => setAuthor(e.target.value)} 
                    />
                  </div>
                  <div className="form-group">
                    <label>{t.uploader.abbrevLabel}</label>
                    <input 
                      type="text" 
                      className="form-input" 
                      value={abbreviation} 
                      onChange={(e) => setAbbreviation(e.target.value.toUpperCase().replace(/\s+/g, ''))} 
                      maxLength={20}
                      required 
                    />
                  </div>
                  
                  {!critiqueResult.has_token && (
                    <div className="form-group">
                      <label>{t.uploader.splitLabel}</label>
                      <div style={{ display: 'flex', gap: '12px', alignItems: 'center', height: '100%' }}>
                        <input 
                          type="checkbox" 
                          checked={splitByHeading} 
                          onChange={(e) => setSplitByHeading(e.target.checked)} 
                          style={{ width: '20px', height: '20px', cursor: 'pointer' }}
                        />
                        <select 
                          className="form-input" 
                          value={headingLevel} 
                          onChange={(e) => setHeadingLevel(Number(e.target.value))}
                          disabled={!splitByHeading}
                          style={{ padding: '6px 12px' }}
                        >
                          <option value="1">Heading 1</option>
                          <option value="2">Heading 2</option>
                          <option value="3">Heading 3</option>
                        </select>
                      </div>
                    </div>
                  )}
                </div>

                {/* Botões de Ação */}
                <div style={{ display: 'flex', gap: '16px', marginTop: '32px' }}>
                  <button 
                    type="button" 
                    className="btn-pricing" 
                    style={{ margin: 0, flex: 1 }} 
                    onClick={() => { setFile(null); setCritiqueResult(null); }}
                  >
                    {lang === 'pt' ? 'Trocar Arquivo' : 'Change File'}
                  </button>
                  
                  {!convertedFileUrl && (
                    <button 
                      type="submit" 
                      className="btn-primary" 
                      style={{ flex: 2, justifyContent: 'center' }} 
                      disabled={converting}
                    >
                      {converting ? t.uploader.converting : t.uploader.convertBtn}
                    </button>
                  )}
                </div>
              </form>

              {/* Resultado Pronto para Download */}
              {convertedFileUrl && (
                <div className="suggestion-item info" style={{ marginTop: '32px', padding: '24px', borderLeftColor: 'var(--success-color)' }}>
                  <div className="sug-header" style={{ color: 'var(--success-color)', fontSize: '16px', marginBottom: '12px' }}>
                    ✅ {t.uploader.success}
                  </div>
                  <a 
                    href={convertedFileUrl} 
                    download={convertedFilename} 
                    className="btn-primary" 
                    style={{ width: '100%', justifyContent: 'center', backgroundColor: 'var(--success-color)', boxShadow: '0 4px 14px rgba(16, 185, 129, 0.4)' }}
                  >
                    📥 {t.uploader.downloadBtn}
                  </a>
                </div>
              )}
            </div>
          )}
        </div>
      </section>

      {/* Features Grid */}
      <section id="features" className="features-section app-container">
        <div className="section-header">
          <h2>{t.features.title}</h2>
          <p>{t.features.subtitle}</p>
        </div>
        <div className="features-grid">
          {t.features.list.map((feat, idx) => (
            <div key={idx} className="feature-card">
              <div className="feature-icon">
                {idx === 0 ? '⚙️' : idx === 1 ? '🔗' : idx === 2 ? '🎨' : '🛡️'}
              </div>
              <h3>{feat.title}</h3>
              <p>{feat.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Pricing Cards */}
      <section id="pricing" className="pricing-section app-container">
        <div className="section-header">
          <h2>{t.pricing.title}</h2>
          <p>{t.pricing.subtitle}</p>
        </div>
        <div className="pricing-grid">
          {/* Card Grátis */}
          <div className="pricing-card">
            <h3 className="plan-name">{t.pricing.free.name}</h3>
            <div className="plan-price-container">
              <span className="plan-price">{t.pricing.free.price}</span>
              <span className="plan-period">/ {t.pricing.free.period}</span>
            </div>
            <p className="plan-desc">{t.pricing.free.desc}</p>
            <ul className="plan-features-list">
              {t.pricing.free.features.map((f, i) => <li key={i}>{f}</li>)}
            </ul>
            <button onClick={() => window.scrollTo(0, 500)} className="btn-pricing">
              {t.pricing.free.cta}
            </button>
          </div>

          {/* Card Crédito Avulso */}
          <div className="pricing-card">
            <h3 className="plan-name">{t.pricing.single.name}</h3>
            <div className="plan-price-container">
              <span className="plan-price">{t.pricing.single.price}</span>
              <span className="plan-period">/ {t.pricing.single.period}</span>
            </div>
            <p className="plan-desc">{t.pricing.single.desc}</p>
            <ul className="plan-features-list">
              {t.pricing.single.features.map((f, i) => <li key={i}>{f}</li>)}
            </ul>
            <button onClick={() => handlePayment('single')} className="btn-pricing">
              {t.pricing.single.cta}
            </button>
          </div>

          {/* Card Mensal */}
          <div className="pricing-card premium">
            <h3 className="plan-name">{t.pricing.monthly.name}</h3>
            <div className="plan-price-container">
              <span className="plan-price">{t.pricing.monthly.price}</span>
              <span className="plan-period">/ {t.pricing.monthly.period}</span>
            </div>
            <p className="plan-desc">{t.pricing.monthly.desc}</p>
            <ul className="plan-features-list">
              {t.pricing.monthly.features.map((f, i) => <li key={i}>{f}</li>)}
            </ul>
            <button onClick={() => handlePayment('monthly')} className="btn-pricing">
              {t.pricing.monthly.cta}
            </button>
          </div>

          {/* Card Anual */}
          <div className="pricing-card">
            <h3 className="plan-name">{t.pricing.yearly.name}</h3>
            <div className="plan-price-container">
              <span className="plan-price">{t.pricing.yearly.price}</span>
              <span className="plan-period">/ {t.pricing.yearly.period}</span>
            </div>
            <p className="plan-desc">{t.pricing.yearly.desc}</p>
            <ul className="plan-features-list">
              {t.pricing.yearly.features.map((f, i) => <li key={i}>{f}</li>)}
            </ul>
            <button onClick={() => handlePayment('yearly')} className="btn-pricing">
              {t.pricing.yearly.cta}
            </button>
          </div>
        </div>
      </section>

      {/* FAQ Accordion */}
      <section id="faq" className="faq-section app-container">
        <div className="section-header">
          <h2>{t.faq.title}</h2>
        </div>
        <div className="faq-list">
          {t.faq.list.map((faq, idx) => (
            <div key={idx} className="faq-item">
              <div className="faq-question" onClick={() => toggleFaq(idx)}>
                <span>{faq.q}</span>
                <span>{faqOpen === idx ? '▲' : '▼'}</span>
              </div>
              {faqOpen === idx && (
                <div className="faq-answer">
                  <p>{faq.a}</p>
                </div>
              )}
            </div>
          ))}
        </div>
      </section>

      {/* Footer */}
      <footer className="footer app-container">
        <p>{t.footer}</p>
      </footer>
    </>
  );
}
