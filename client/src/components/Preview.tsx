interface Issue {
  issue_type: string;
  description: string;
  location?: string;
  suggestion: string;
}

interface PreviewProps {
  filename: string;
  fileSize: number;
  isFormatting: boolean;
  isComplete: boolean;
  issuesFound: Issue[];
  issuesFixed: number;
}

export function Preview({ 
  filename, 
  fileSize, 
  isFormatting, 
  isComplete, 
  issuesFound, 
  issuesFixed 
}: PreviewProps) {
  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
      {/* File Info Header */}
      <div className="p-4 bg-gray-50 border-b border-gray-200">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-blue-100 rounded-lg">
            <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <div className="flex-1 min-w-0">
            <p className="font-medium text-gray-800 truncate">{filename}</p>
            <p className="text-sm text-gray-500">{formatFileSize(fileSize)}</p>
          </div>
          {isComplete && (
            <span className="px-2 py-1 bg-green-100 text-green-700 text-sm font-medium rounded-full">
              ✓ Complete
            </span>
          )}
        </div>
      </div>

      {/* Status Section */}
      <div className="p-4">
        {isFormatting ? (
          <div className="flex flex-col items-center py-8">
            <div className="relative">
              <div className="w-16 h-16 border-4 border-blue-200 rounded-full"></div>
              <div className="absolute top-0 left-0 w-16 h-16 border-4 border-blue-600 rounded-full animate-spin border-t-transparent"></div>
            </div>
            <p className="mt-4 text-gray-600 font-medium">Formatting your document...</p>
            <p className="text-sm text-gray-400 mt-1">This may take a moment</p>
          </div>
        ) : isComplete ? (
          <div>
            {/* Success Stats */}
            <div className="grid grid-cols-2 gap-4 mb-4">
              <div className="p-4 bg-green-50 rounded-lg text-center">
                <p className="text-2xl font-bold text-green-600">{issuesFixed}</p>
                <p className="text-sm text-green-700">Issues Fixed</p>
              </div>
              <div className="p-4 bg-yellow-50 rounded-lg text-center">
                <p className="text-2xl font-bold text-yellow-600">{issuesFound.length}</p>
                <p className="text-sm text-yellow-700">Warnings</p>
              </div>
            </div>

            {/* Issues List */}
            {issuesFound.length > 0 && (
              <div className="mt-4">
                <h4 className="text-sm font-medium text-gray-700 mb-2">Attention Needed:</h4>
                <ul className="space-y-2">
                  {issuesFound.map((issue, index) => (
                    <li key={index} className="flex items-start gap-2 text-sm">
                      <span className="text-yellow-500 mt-0.5">⚠️</span>
                      <div>
                        <p className="text-gray-700">{issue.description}</p>
                        {issue.suggestion && (
                          <p className="text-gray-500 text-xs mt-0.5">
                            💡 {issue.suggestion}
                          </p>
                        )}
                      </div>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {issuesFound.length === 0 && (
              <div className="text-center py-4">
                <span className="text-4xl">🎉</span>
                <p className="text-gray-600 mt-2">Document formatted successfully!</p>
              </div>
            )}
          </div>
        ) : (
          <div className="text-center py-8 text-gray-500">
            <p>Select formatting options and click "Format Document" to begin</p>
          </div>
        )}
      </div>
    </div>
  );
}
