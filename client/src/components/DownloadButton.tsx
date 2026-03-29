interface DownloadButtonProps {
  downloadUrl: string | null;
  isReady: boolean;
  onDownload: () => void;
  onReset: () => void;
}

export function DownloadButton({ downloadUrl, isReady, onDownload, onReset }: DownloadButtonProps) {
  if (!isReady) {
    return null;
  }

  return (
    <div className="flex flex-col sm:flex-row gap-3">
      <a
        href={downloadUrl || '#'}
        onClick={onDownload}
        className={`
          flex-1 flex items-center justify-center gap-2 px-6 py-3 rounded-lg
          font-medium text-white transition-all duration-200
          ${downloadUrl 
            ? 'bg-green-600 hover:bg-green-700 shadow-lg shadow-green-200' 
            : 'bg-gray-400 cursor-not-allowed'}
        `}
      >
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
        </svg>
        Download Formatted Document
      </a>
      
      <button
        onClick={onReset}
        className="px-6 py-3 rounded-lg border border-gray-300 text-gray-700 font-medium hover:bg-gray-50 transition-all duration-200"
      >
        Format Another
      </button>
    </div>
  );
}
