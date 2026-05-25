export type Language = 'en' | 'es' | 'pt';

export interface TranslationDict {
  brand: string;
  nav: {
    uploader: string;
    features: string;
    pricing: string;
    faq: string;
  };
  hero: {
    tagline: string;
    title: string;
    subtitle: string;
    cta: string;
  };
  uploader: {
    title: string;
    dragDrop: string;
    browse: string;
    analyzing: string;
    critiqueHeader: string;
    metadata: string;
    titleLabel: string;
    authorLabel: string;
    abbrevLabel: string;
    splitLabel: string;
    convertBtn: string;
    converting: string;
    downloadBtn: string;
    success: string;
    noTokenWarning: string;
    sectionsFound: string;
    refsFound: string;
  };
  features: {
    title: string;
    subtitle: string;
    list: {
      title: string;
      desc: string;
    }[];
  };
  pricing: {
    title: string;
    subtitle: string;
    free: {
      name: string;
      price: string;
      period: string;
      desc: string;
      cta: string;
      features: string[];
    };
    single: {
      name: string;
      price: string;
      period: string;
      desc: string;
      cta: string;
      features: string[];
    };
    monthly: {
      name: string;
      price: string;
      period: string;
      desc: string;
      cta: string;
      features: string[];
    };
    yearly: {
      name: string;
      price: string;
      period: string;
      desc: string;
      cta: string;
      features: string[];
    };
  };
  faq: {
    title: string;
    list: {
      q: string;
      a: string;
    }[];
  };
  footer: string;
}

export const translations: Record<Language, TranslationDict> = {
  en: {
    brand: "MySword Tools",
    nav: {
      uploader: "Converter",
      features: "Features",
      pricing: "Pricing",
      faq: "FAQ"
    },
    hero: {
      tagline: "The Ultimate Companion for Android Bible Studies",
      title: "Convert Word Documents to MySword Format in Seconds",
      subtitle: "Import your .docx study files, automatically extract metadata, format colors, link bible verses, and split topics perfectly with our intelligent parser.",
      cta: "Start Converting Free"
    },
    uploader: {
      title: "Interactive Document Converter",
      dragDrop: "Drag and drop your .docx file here or",
      browse: "browse files",
      analyzing: "Analyzing document structure...",
      critiqueHeader: "Validation Report & Structure",
      metadata: "Extracted Metadata",
      titleLabel: "Journal Title",
      authorLabel: "Author",
      abbrevLabel: "Abbreviation (Max 20 chars)",
      splitLabel: "Split by headings (Fallback)",
      convertBtn: "Generate .jor.mybible File",
      converting: "Generating database...",
      downloadBtn: "Download MySword File",
      success: "Conversion completed successfully!",
      noTokenWarning: "Warning: No @@---@@ tokens found. The document will be split by heading styles or saved as a single section.",
      sectionsFound: "Entries to be created:",
      refsFound: "Bible links to be generated:"
    },
    features: {
      title: "Engineered for Bible Teachers",
      subtitle: "Everything you need to convert lessons, commentaries, and devotionals into study modules.",
      list: [
        {
          title: "Token Division (@@---@@)",
          desc: "Separate lessons or days explicitly by inserting @@---@@ on an empty line in Word. Zero parsing mistakes."
        },
        {
          title: "Auto Bible Verse Linking",
          desc: "Our engine automatically detects verse references (like Gen 1:1 or Jn 3:16) and generates native MySword links."
        },
        {
          title: "Preserve Formatting",
          desc: "Retain bold, italics, underlines, text colors, and complex tables converted directly to optimized HTML."
        },
        {
          title: "Fast Validation Check",
          desc: "Upload and instantly see missing metadata, chapter counts, and potential warnings before purchasing or converting."
        }
      ]
    },
    pricing: {
      title: "Simple, Transparent Pricing",
      subtitle: "Choose the plan that fits your creation frequency.",
      free: {
        name: "Free",
        price: "$0",
        period: "forever",
        desc: "For casual users and testing files.",
        cta: "Start Free",
        features: ["1 conversion per day", "Up to 3 sections per document", "Basic structure check"]
      },
      single: {
        name: "Pay-As-You-Go",
        price: "$0.99",
        period: "per file",
        desc: "Convert sporadic studies with full access.",
        cta: "Buy Credit",
        features: ["Single conversion token", "Unlimited sections", "All styling & tables", "Full support"]
      },
      monthly: {
        name: "Creator Monthly",
        price: "$3.99",
        period: "month",
        desc: "Perfect for pastors and EBD teachers.",
        cta: "Subscribe Now",
        features: ["Unlimited conversions", "Unlimited sections", "Priority support", "No daily limits", "Cancel anytime"]
      },
      yearly: {
        name: "Creator Yearly",
        price: "$29.99",
        period: "year",
        desc: "Saves 37% over the monthly plan.",
        cta: "Subscribe & Save",
        features: ["Unlimited conversions", "Unlimited sections", "Priority support", "Best value (equivalent to 4 free months)"]
      }
    },
    faq: {
      title: "Frequently Asked Questions",
      list: [
        {
          q: "Where do I copy the converted file on my Android device?",
          a: "Connect your phone to a computer and copy the .jor.mybible file into the directory: /storage/emulated/0/mysword/journals/ (or inside the 'journals' folder inside the MySword root folder)."
        },
        {
          q: "How do I trigger the study division properly?",
          a: "Just write @@---@@ on an empty line in Word right before the title of each new lesson or article. The parser will split the document exactly at those points, naming each section with the text on the line immediately following the token."
        },
        {
          q: "Do I need a premium version of MySword to use these journals?",
          a: "No, journals are fully supported in the free version of MySword. However, donating to the MySword project unlocks premium layout features inside their app."
        },
        {
          q: "Are references formatted automatically?",
          a: "Yes. Text patterns like 'John 3:16' or abbreviated forms like 'Gen 1:1-3' in Portuguese, Spanish, or English are converted to clickable links that open the verse window directly in MySword."
        }
      ]
    },
    footer: "© 2026 MySword Tools. All rights reserved. Not affiliated with the official MySword Android Application."
  },
  es: {
    brand: "MySword Tools",
    nav: {
      uploader: "Convertidor",
      features: "Características",
      pricing: "Precios",
      faq: "Preguntas"
    },
    hero: {
      tagline: "El compañero definitivo para estudios bíblicos en Android",
      title: "Convierta documentos de Word a formato MySword en segundos",
      subtitle: "Importe sus archivos de estudio .docx, extraiga metadatos automáticamente, formatee colores, enlace versículos bíblicos y divida temas perfectamente con nuestro analizador inteligente.",
      cta: "Comience a Convertir Gratis"
    },
    uploader: {
      title: "Convertidor Interactivo de Documentos",
      dragDrop: "Arrastre y suelte su archivo .docx aquí o",
      browse: "busque en sus archivos",
      analyzing: "Analizando la estructura del documento...",
      critiqueHeader: "Informe de Validación y Estructura",
      metadata: "Metadatos Extraídos",
      titleLabel: "Título del Diario",
      authorLabel: "Autor",
      abbrevLabel: "Abreviatura (Máx 20 caracteres)",
      splitLabel: "Dividir por encabezados (Alternativo)",
      convertBtn: "Generar archivo .jor.mybible",
      converting: "Generando base de datos...",
      downloadBtn: "Descargar archivo MySword",
      success: "¡Conversión completada con éxito!",
      noTokenWarning: "Advertencia: No se encontraron tokens @@---@@. El documento se dividirá por estilos de título o se guardará como una sola sección.",
      sectionsFound: "Entradas a crear:",
      refsFound: "Enlaces bíblicos a generar:"
    },
    features: {
      title: "Diseñado para Maestros de la Biblia",
      subtitle: "Todo lo que necesita para convertir lecciones, comentarios y devocionales en módulos de estudio.",
      list: [
        {
          title: "División por Token (@@---@@)",
          desc: "Separe lecciones o días de forma explícita insertando @@---@@ en una línea vacía en Word. Cero errores de análisis."
        },
        {
          title: "Enlaces Bíblicos Automáticos",
          desc: "Nuestro motor detecta automáticamente referencias a versículos (como Gén 1:1 o Juan 3:16) y genera enlaces nativos de MySword."
        },
        {
          title: "Preservación del Formato",
          desc: "Conserve negritas, cursivas, subrayados, colores de texto y tablas complejas convertidas directamente a HTML optimizado."
        },
        {
          title: "Validación Rápida",
          desc: "Suba su archivo y vea instantáneamente metadados faltantes, recuentos de capítulos y posibles advertencias antes de convertir."
        }
      ]
    },
    pricing: {
      title: "Precios Simples y Transparentes",
      subtitle: "Elija el plan que mejor se adapte a su frecuencia de creación.",
      free: {
        name: "Gratis",
        price: "$0",
        period: "siempre",
        desc: "Para usuarios ocasionales y pruebas de archivos.",
        cta: "Comenzar Gratis",
        features: ["1 conversión por día", "Hasta 3 secciones por documento", "Validación básica de estructura"]
      },
      single: {
        name: "Pago por Uso",
        price: "$0.99",
        period: "por archivo",
        desc: "Convierta estudios esporádicos con acceso total.",
        cta: "Comprar Crédito",
        features: ["1 token de conversión", "Secciones ilimitadas", "Todos los estilos y tablas", "Soporte completo"]
      },
      monthly: {
        name: "Creador Mensual",
        price: "$3.99",
        period: "mes",
        desc: "Perfecto para pastores y maestros de escuela bíblica.",
        cta: "Suscribirse Ahora",
        features: ["Conversiones ilimitadas", "Secciones ilimitadas", "Soporte prioritario", "Sin límites diarios", "Cancele cuando quiera"]
      },
      yearly: {
        name: "Creador Anual",
        price: "$29.99",
        period: "año",
        desc: "Ahorre un 37% en comparación con el plan mensual.",
        cta: "Suscribirse y Ahorrar",
        features: ["Conversiones ilimitadas", "Secciones ilimitadas", "Soporte prioritario", "Mejor valor (equivalente a 4 meses gratis)"]
      }
    },
    faq: {
      title: "Preguntas Frecuentes",
      list: [
        {
          q: "¿Dónde copio el archivo convertido en mi dispositivo Android?",
          a: "Conecte su teléfono a una computadora y copie el archivo .jor.mybible en la ruta: /storage/emulated/0/mysword/journals/ (o dentro de la carpeta 'journals' en la raíz de la aplicación MySword)."
        },
        {
          q: "¿Cómo configuro la división de estudios correctamente?",
          a: "Simplemente escriba @@---@@ en una línea vacía en Word justo antes del título de cada nueva lección. El convertidor dividirá el documento en esos puntos, usando el texto de la línea siguiente como título de la sección."
        },
        {
          q: "¿Necesito una versión de pago de MySword para usar estos diarios?",
          a: "No, los diarios son totalmente compatibles con la versión gratuita de MySword. Sin embargo, donar al proyecto MySword desbloquea funciones de visualización avanzadas en su aplicación."
        },
        {
          q: "¿Las referencias bíblicas se enlazan automáticamente?",
          a: "Sí. Los patrones de texto como 'Juan 3:16' o abreviaturas como 'Gén 1:1-3' en español, inglés o portugués se convierten en enlaces interactivos que abren los versículos en MySword."
        }
      ]
    },
    footer: "© 2026 MySword Tools. Todos los derechos reservados. No afiliado con la aplicación oficial de Android MySword."
  },
  pt: {
    brand: "MySword Tools",
    nav: {
      uploader: "Conversor",
      features: "Recursos",
      pricing: "Preços",
      faq: "Perguntas"
    },
    hero: {
      tagline: "O companheiro definitivo para estudos bíblicos no Android",
      title: "Converta documentos do Word para o formato MySword em segundos",
      subtitle: "Importe seus arquivos de estudo .docx, extraia metadados automaticamente, preserve a formatação de cores, crie links para versículos bíblicos e separe lições perfeitamente com nosso parser inteligente.",
      cta: "Começar a Converter Grátis"
    },
    uploader: {
      title: "Conversor Interativo de Documentos",
      dragDrop: "Arraste e solte seu arquivo .docx aqui ou",
      browse: "escolha nos seus arquivos",
      analyzing: "Analisando a estrutura do documento...",
      critiqueHeader: "Relatório de Validação & Estrutura",
      metadata: "Metadados Extraídos",
      titleLabel: "Título do Journal",
      authorLabel: "Autor",
      abbrevLabel: "Abreviação (Máx 20 caracteres)",
      splitLabel: "Dividir por cabeçalhos (Secundário)",
      convertBtn: "Gerar arquivo .jor.mybible",
      converting: "Gerando banco de dados...",
      downloadBtn: "Baixar Arquivo MySword",
      success: "Conversão concluída com sucesso!",
      noTokenWarning: "Aviso: Nenhum token @@---@@ encontrado. O documento será dividido por estilos de título ou salvo como uma única seção.",
      sectionsFound: "Entradas a serem criadas:",
      refsFound: "Links bíblicos a serem gerados:"
    },
    features: {
      title: "Projetado para Professores da Bíblia",
      subtitle: "Tudo o que você precisa para transformar lições, esboços e devocionais em módulos de estudo.",
      list: [
        {
          title: "Divisão por Token (@@---@@)",
          desc: "Separe as lições ou dias explicitamente inserindo @@---@@ em uma linha vazia no Word. Zero erros de divisão."
        },
        {
          title: "Links Bíblicos Automáticos",
          desc: "Nosso sistema detecta automaticamente referências bíblicas (ex: João 3:16 ou Gn 1:1) e gera os links nativos do MySword."
        },
        {
          title: "Preservação de Formatação",
          desc: "Mantenha negritos, itálicos, sublinhados, cores de texto e tabelas complexas convertidas de forma limpa para HTML."
        },
        {
          title: "Validação Pré-Voo",
          desc: "Suba o arquivo e veja na hora metadados ausentes, contagem de capítulos e avisos de formatação antes de converter."
        }
      ]
    },
    pricing: {
      title: "Preços Simples e Transparentes",
      subtitle: "Escolha o plano ideal para a sua frequência de criação.",
      free: {
        name: "Gratuito",
        price: "R$ 0",
        period: "sempre",
        desc: "Para usuários ocasionais ou testes rápidos.",
        cta: "Começar Grátis",
        features: ["1 conversão por dia", "Até 3 seções por documento", "Análise básica de estrutura"]
      },
      single: {
        name: "Crédito Avulso",
        price: "R$ 4,90",
        period: "por arquivo",
        desc: "Converta estudos avulsos com acesso total.",
        cta: "Comprar Crédito",
        features: ["1 token de conversão", "Seções ilimitadas", "Todos os estilos e tabelas", "Suporte completo"]
      },
      monthly: {
        name: "Criador Mensal",
        price: "R$ 19,90",
        period: "mês",
        desc: "Perfeito para pastores e professores de EBD.",
        cta: "Assinar Agora",
        features: ["Conversões ilimitadas", "Seções ilimitadas", "Suporte prioritário", "Sem limites diários", "Cancele a qualquer momento"]
      },
      yearly: {
        name: "Criador Anual",
        price: "R$ 149,90",
        period: "ano",
        desc: "Economize equivalentemente a 4 meses grátis.",
        cta: "Assinar e Economizar",
        features: ["Conversões ilimitadas", "Seções ilimitadas", "Suporte prioritário", "Melhor custo-benefício"]
      }
    },
    faq: {
      title: "Perguntas Frequentes",
      list: [
        {
          q: "Como copio o arquivo convertido para o meu dispositivo Android?",
          a: "Conecte seu celular ao computador e copie o arquivo .jor.mybible para a pasta: /storage/emulated/0/mysword/journals/ (ou dentro da pasta 'journals' na pasta raiz do MySword)."
        },
        {
          q: "Como configurar a divisão de estudos corretamente?",
          a: "Basta escrever @@---@@ em uma linha vazia no Word imediatamente antes do título de cada lição. O conversor dividirá o documento ali, adotando o texto da linha seguinte como o título da lição."
        },
        {
          q: "Preciso de uma versão paga do MySword para rodar esses diários?",
          a: "Não, diários e anotações são totalmente suportados na versão gratuita do MySword. No entanto, doações voluntárias ao projeto MySword liberam layouts adicionais em seu dispositivo."
        },
        {
          q: "As referências bíblicas viram links clicáveis automaticamente?",
          a: "Sim. Padrões textuais como 'João 3:16' ou abreviações brasileiras clássicas (como 'Gn 1:1') são convertidos para links clicáveis que abrem a tela de leitura de versículos no MySword."
        }
      ]
    },
    footer: "© 2026 MySword Tools. Todos os direitos reservados. Não afiliado ao aplicativo Android oficial MySword."
  }
};
