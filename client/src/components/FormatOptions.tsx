interface FormatOptionsProps {
  options: {
    fix_title_page: boolean;
    fix_headings: boolean;
    fix_citations: boolean;
    fix_references: boolean;
    fix_spacing: boolean;
    generate_toc: boolean;
    use_ai_enhancement: boolean;
  };
  onOptionsChange: (options: FormatOptionsProps['options']) => void;
  aiAvailable: boolean;
}

export function FormatOptions({ options, onOptionsChange, aiAvailable }: FormatOptionsProps) {
  const handleChange = (key: keyof FormatOptionsProps['options']) => {
    onOptionsChange({
      ...options,
      [key]: !options[key]
    });
  };

  const optionItems = [
    {
      key: 'fix_title_page' as const,
      label: 'Title Page',
      description: 'Generate APA 7th edition title page',
      icon: '📄'
    },
    {
      key: 'fix_headings' as const,
      label: 'Headings',
      description: 'Format headings to 5-level APA style (centered/bold for L1, left/bold for L2, etc.)',
      icon: '📑'
    },
    {
      key: 'fix_citations' as const,
      label: 'Citations',
      description: 'Fix in-text citation formatting',
      icon: '📝'
    },
    {
      key: 'fix_references' as const,
      label: 'References',
      description: 'Sort and format reference list with hanging indent',
      icon: '📚'
    },
    {
      key: 'fix_spacing' as const,
      label: 'Spacing & Fonts',
      description: 'Apply double-spacing, Times New Roman 12pt, 1" margins',
      icon: '📏'
    },
    {
      key: 'generate_toc' as const,
      label: 'Table of Contents',
      description: 'Generate TOC, List of Figures, List of Tables',
      icon: '📋'
    },
    {
      key: 'use_ai_enhancement' as const,
      label: 'AI Enhancement',
      description: aiAvailable 
        ? 'Use AI to improve academic tone' 
        : 'Set OPENAI_API_KEY to enable',
      icon: '🤖',
      disabled: !aiAvailable
    }
  ];

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
        <span>⚙️</span> Formatting Options
      </h3>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {optionItems.map((item) => (
          <label
            key={item.key}
            className={`
              flex items-start gap-3 p-3 rounded-lg border cursor-pointer
              transition-all duration-200
              ${options[item.key] && !item.disabled
                ? 'border-blue-500 bg-blue-50' 
                : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'}
              ${item.disabled ? 'opacity-50 cursor-not-allowed' : ''}
            `}
          >
            <input
              type="checkbox"
              checked={options[item.key]}
              onChange={() => !item.disabled && handleChange(item.key)}
              disabled={item.disabled}
              className="mt-1 h-4 w-4 text-blue-600 rounded border-gray-300 focus:ring-blue-500"
            />
            <div className="flex-1">
              <div className="flex items-center gap-2">
                <span>{item.icon}</span>
                <span className="font-medium text-gray-800">{item.label}</span>
              </div>
              <p className="text-sm text-gray-500 mt-0.5">{item.description}</p>
            </div>
          </label>
        ))}
      </div>

      {/* Select All / Deselect All */}
      <div className="mt-4 flex gap-2">
        <button
          onClick={() => onOptionsChange({
            ...options,
            fix_title_page: true,
            fix_headings: true,
            fix_citations: true,
            fix_references: true,
            fix_spacing: true,
            generate_toc: true,
          })}
          className="text-sm text-blue-600 hover:text-blue-700 font-medium"
        >
          Select All
        </button>
        <span className="text-gray-300">|</span>
        <button
          onClick={() => onOptionsChange({
            ...options,
            fix_title_page: false,
            fix_headings: false,
            fix_citations: false,
            fix_references: false,
            fix_spacing: false,
            generate_toc: false,
          })}
          className="text-sm text-gray-500 hover:text-gray-700"
        >
          Deselect All
        </button>
      </div>
    </div>
  );
}
