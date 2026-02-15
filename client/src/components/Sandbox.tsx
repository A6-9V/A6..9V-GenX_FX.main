import React, { useEffect, useRef } from 'react';
import sdk from '@stackblitz/sdk';

const Sandbox: React.FC = () => {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (containerRef.current) {
      sdk.embedProjectId(
        containerRef.current,
        'stackblitz-webcontainer-api-starter-uwbpod2b',
        {
          forceEmbedLayout: true,
          openFile: 'README.md',
          height: 600,
          width: '100%',
        }
      );
    }
  }, []);

  return (
    <div className="max-w-6xl mx-auto bg-white rounded-lg shadow-md p-6">
      <h2 className="text-3xl font-bold mb-6 text-gray-900">Developer Sandbox</h2>
      <p className="text-gray-600 mb-4">
        Explore the WebContainer API and test your ideas in this integrated environment.
      </p>
      <div
        ref={containerRef}
        className="w-full border border-gray-200 rounded-lg overflow-hidden"
        style={{ height: '600px' }}
      >
        Loading Sandbox...
      </div>
    </div>
  );
};

export default Sandbox;
