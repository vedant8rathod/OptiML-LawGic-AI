import React from 'react';
import { Badge } from '@/components/ui/badge';
import { Card } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';
import { useLanguage } from '@/contexts/LanguageContext';
import {
  FileText,
  AlertTriangle, 
  BookOpen, 
  Scale,
  Shield,
  CheckCircle2,
  Users,
  Calendar,
  Briefcase
} from 'lucide-react';

interface ResponseFormatterProps {
  content: string;
  title?: string;
}

const ResponseFormatter: React.FC<ResponseFormatterProps> = ({ content, title }) => {
  const { t } = useLanguage();
  
  // Translation mapping for common response headers
  const translateHeader = (header: string): string => {
    const headerMappings: Record<string, string> = {
      'risk': t('response.risk'),
      'risks': t('response.risks'),
      'disclaimer': t('response.disclaimer'),
      'warning': t('response.warning'),
      'warnings': t('response.warnings'),
      'legal analysis': t('response.legalAnalysis'),
      'case summary': t('response.caseSummary'),
      'document summary': t('response.documentSummary'),
      'recommendation': t('response.recommendation'),
      'recommendations': t('response.recommendations'),
      'next steps': t('response.nextSteps'),
      'legal implications': t('response.legalImplications'),
      'compliance': t('response.compliance'),
      'jurisdiction': t('response.jurisdiction'),
      'relevant laws': t('response.relevantLaws'),
      'key points': t('response.keyPoints'),
      'analysis': t('response.analysis'),
      'summary': t('response.summary'),
      'conclusion': t('response.conclusion'),
      'important note': t('response.importantNote'),
      'legal advice': t('response.legalAdvice'),
      'court decisions': t('response.courtDecisions'),
      'statute': t('response.statute'),
      'statutes': t('response.statutes'),
      'recent developments': t('response.recentDevelopments'),
      'action required': t('response.actionRequired'),
      'tenant rights': t('response.tenantRights'),
      'rental laws': t('response.rentalLaws'),
      'employment law': t('response.employmentLaw'),
      'contract terms': t('response.contractTerms'),
      'legal rights': t('response.legalRights'),
      'category': t('response.category'),
      'key findings': t('response.keyFindings'),
      'risk assessment': t('response.riskAssessment'),
      'level': t('response.level'),
      'factors': t('response.factors'),
      'compliance issues': t('response.complianceIssues'),
      'next steps': t('response.nextSteps')
    };
    
    const lowerHeader = header.toLowerCase();
    return headerMappings[lowerHeader] || header;
  };
  
  const formatContent = (text: string) => {
    // Handle simple text content that may contain markdown formatting
    const lines = text.split('\n');
    const formattedLines: React.ReactNode[] = [];
    
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      
      // Check if line starts with ** (bold header)
      const boldHeaderMatch = line.match(/^\*\*([^*]+)\*\*:?\s*(.*)$/);
      if (boldHeaderMatch) {
        const [, header, remainder] = boldHeaderMatch;
        
        formattedLines.push(
          <div key={i} className="mb-4">
            <div className="flex items-center gap-2 mb-2">
              {getIconForHeader(header)}
              <h3 className="text-lg font-bold text-gray-900 dark:text-gray-100">
                {translateHeader(header)}
              </h3>
            </div>
            {remainder && (
              <div className="ml-6">
                <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
                  {formatInlineText(remainder)}
                </p>
              </div>
            )}
          </div>
        );
        continue;
      }
      
      // Handle empty lines as spacing
      if (!line.trim()) {
        formattedLines.push(<div key={i} className="mb-2"></div>);
        continue;
      }
      
      // Format regular lines
      formattedLines.push(
        <div key={i} className="mb-2">
          {formatLineContent(line)}
        </div>
      );
    }
    
    return formattedLines;
  };

  const formatLineContent = (line: string) => {
    // Handle bullet points
    if (line.trim().startsWith('•') || line.trim().startsWith('-')) {
      return (
        <div className="flex items-start gap-2">
          <div className="w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0"></div>
          <span className="text-gray-700 dark:text-gray-300 leading-relaxed">
            {formatInlineText(line.replace(/^[•-]\s*/, ''))}
          </span>
        </div>
      );
    }
    
    // Handle numbered lists
    if (line.match(/^\d+\.\s/)) {
      return (
        <div className="flex items-start gap-3">
          <span className="text-blue-600 font-semibold text-sm bg-blue-50 dark:bg-blue-900/30 px-2 py-1 rounded-full">
            {line.match(/^(\d+)/)?.[1]}
          </span>
          <span className="text-gray-700 dark:text-gray-300 leading-relaxed">
            {formatInlineText(line.replace(/^\d+\.\s*/, ''))}
          </span>
        </div>
      );
    }
    
    // Handle case names (italicized legal cases)
    if (line.includes(' v. ') || line.includes(' vs. ')) {
      return (
        <div className="p-3 bg-amber-50 dark:bg-amber-900/20 border-l-4 border-amber-400 rounded-r">
          <span className="text-gray-800 dark:text-gray-200 italic font-medium">
            {formatInlineText(line)}
          </span>
        </div>
      );
    }
    
    // Regular text
    return (
      <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
        {formatInlineText(line)}
      </p>
    );
  };


  const formatInlineText = (text: string) => {
    // Handle **bold** text
    const parts = text.split(/(\*\*[^*]+\*\*)/g);
    return parts.map((part, index) => {
      if (part.startsWith('**') && part.endsWith('**')) {
        return (
          <strong key={index} className="font-semibold text-gray-900 dark:text-gray-100">
            {part.slice(2, -2)}
          </strong>
        );
      }
      return part;
    });
  };

  const getIconForHeader = (header: string) => {
    const headerLower = header.toLowerCase();
    
    if (headerLower.includes('document') || headerLower.includes('summary')) {
      return <FileText className="w-5 h-5 text-blue-600" />;
    }
    if (headerLower.includes('risk') || headerLower.includes('warning')) {
      return <AlertTriangle className="w-5 h-5 text-red-600" />;
    }
    if (headerLower.includes('case') || headerLower.includes('legal')) {
      return <Scale className="w-5 h-5 text-purple-600" />;
    }
    if (headerLower.includes('statute') || headerLower.includes('law')) {
      return <BookOpen className="w-5 h-5 text-green-600" />;
    }
    if (headerLower.includes('compliance') || headerLower.includes('regulation')) {
      return <Shield className="w-5 h-5 text-orange-600" />;
    }
    if (headerLower.includes('recommend') || headerLower.includes('next')) {
      return <CheckCircle2 className="w-5 h-5 text-emerald-600" />;
    }
    if (headerLower.includes('jurisdiction') || headerLower.includes('court')) {
      return <Users className="w-5 h-5 text-indigo-600" />;
    }
    if (headerLower.includes('remed') || headerLower.includes('action')) {
      return <Briefcase className="w-5 h-5 text-teal-600" />;
    }
    if (headerLower.includes('development') || headerLower.includes('recent')) {
      return <Calendar className="w-5 h-5 text-pink-600" />;
    }
    
    // Default icon
    return <FileText className="w-5 h-5 text-gray-600" />;
  };

  return (
    <Card className="p-6 bg-white dark:bg-gray-800 shadow-lg">
      <div className="space-y-2">
        {formatContent(content)}
      </div>
    </Card>
  );
};

export default ResponseFormatter;