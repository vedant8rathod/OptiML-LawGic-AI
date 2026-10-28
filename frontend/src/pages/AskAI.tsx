import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { Send, Sparkles, Shield, MessageSquare, Upload, Mic } from "lucide-react";
import { toast } from "sonner";
import { apiService } from "@/services/api";
import ResponseFormatter from "@/components/ResponseFormatter";
import { useLanguage } from "@/contexts/LanguageContext";

type AnalysisMode = "predict" | "analyze" | "research";

type ModeConfig = {
  key: AnalysisMode;
  label: string;
  description: string;
  responseTitle: string;
  successMessage: string;
};

// MODE_OPTIONS moved inside component to access translations

// MODE_PLACEHOLDER moved inside component to access translations

const startCase = (value: string): string =>
  value
    .replace(/[_-]+/g, " ")
    .replace(/\s+/g, " ")
    .trim()
    .replace(/\b\w/g, (char) => char.toUpperCase());

const formatPredictionBlock = (prediction: unknown, t: (key: string) => string): string => {
  if (prediction === null || prediction === undefined) {
    return "No insights were returned from the backend.";
  }

  if (typeof prediction === "string") {
    const trimmed = prediction.trim();
    const looksJson = (trimmed.startsWith("{") && trimmed.endsWith("}")) || (trimmed.startsWith("[") && trimmed.endsWith("]"));
    if (looksJson) {
      try {
        const parsed = JSON.parse(trimmed);
        return formatPredictionBlock(parsed);
      } catch {
        // fall through to raw string if JSON parse fails
      }
    }
    return prediction;
  }

  if (typeof prediction === "number" || typeof prediction === "boolean") {
    return String(prediction);
  }

  if (Array.isArray(prediction)) {
    if (prediction.length === 0) {
      return t('common.noItems');
    }

      return prediction
        .map((item) => {
          const value = formatPredictionBlock(item, t);
          return value.startsWith("• ") ? value : `• ${value}`;
        })
        .join("\n");
  }

  if (typeof prediction === "object") {
    const entries = Object.entries(prediction as Record<string, unknown>);
    if (entries.length === 0) {
      return t('common.noDetails');
    }

    return entries
      .map(([key, value]) => {
        const formattedValue = formatPredictionBlock(value, t);
        // Try to translate the key first, fallback to startCase
        const lowerKey = key.toLowerCase().replace(/_/g, ' ');
        const translatedKey = 
          lowerKey === 'document summary' ? t('response.documentSummary') :
          lowerKey === 'category' ? t('response.category') :
          lowerKey === 'disclaimer' ? t('response.disclaimer') :
          lowerKey === 'risk' ? t('response.risk') :
          lowerKey === 'analysis' ? t('response.analysis') :
          lowerKey === 'recommendation' ? t('response.recommendation') :
          lowerKey === 'recommendations' ? t('response.recommendations') :
          lowerKey === 'summary' ? t('response.summary') :
          lowerKey === 'key findings' ? t('response.keyFindings') :
          lowerKey === 'risk assessment' ? t('response.riskAssessment') :
          lowerKey === 'level' ? t('response.level') :
          lowerKey === 'factors' ? t('response.factors') :
          lowerKey === 'compliance issues' ? t('response.complianceIssues') :
          lowerKey === 'next steps' ? t('response.nextSteps') :
          startCase(key);
        return formattedValue.includes("\n")
          ? `**${translatedKey}:**\n${formattedValue}`
          : `**${translatedKey}:** ${formattedValue}`;
      })
      .join("\n\n");
  }

  return String(prediction);
};

const formatAssistantResponse = (
  title: string,
  prediction: unknown,
  t: (key: string) => string,
  meta?: { input?: string; documentId?: string | number }
): string => {
  const sections: string[] = [];

  if (title) {
    sections.push(`**${title}**`);
  }

  if (meta?.input) {
    sections.push(`**${t('common.inputSummary')}:**\n${meta.input}`);
  }

  const predictionBlock = formatPredictionBlock(prediction, t);
  if (predictionBlock) {
    sections.push(predictionBlock);
  }

  if (meta?.documentId !== undefined) {
    sections.push(`${t('common.referenceId')}: ${meta.documentId}`);
  }

  return sections.filter(Boolean).join("\n\n");
};

const AskAI = () => {
  const { t, language } = useLanguage();
  const [analysisMode, setAnalysisMode] = useState<AnalysisMode>("predict");
  
  const MODE_OPTIONS: ModeConfig[] = [
    {
      key: "predict",
      label: t('askAI.quickAnswer'),
      description: t('askAI.quickAnswer.description'),
      responseTitle: t('common.textAnalysisResult'),
      successMessage: t('common.textAnalysisComplete'),
    },
    {
      key: "analyze",
      label: t('askAI.documentVoice'),
      description: t('askAI.documentVoice.description'),
      responseTitle: t('common.comprehensiveAnalysis'),
      successMessage: t('common.documentAnalysisComplete'),
    },
    {
      key: "research",
      label: t('askAI.legalResearch'),
      description: t('askAI.legalResearch.description'),
      responseTitle: t('common.legalResearchSummary'),
      successMessage: t('common.legalResearchReady'),
    },
  ];
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState<Array<{ role: "user" | "assistant"; content: string }>>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [uploadedVoice, setUploadedVoice] = useState<File | null>(null);

  const suggestions = [
    t('suggestions.rental'),
    t('suggestions.tenantRights'),
    t('suggestions.employment'),
    t('suggestions.legalDocument'),
  ];
  
  const MODE_PLACEHOLDER: Record<AnalysisMode, string> = {
    predict: t('askAI.placeholder.predict'),
    analyze: t('askAI.placeholder.analyze'),
    research: t('askAI.placeholder.research'),
  };

  const attachmentsAllowed = analysisMode !== "predict";
  const activeModeConfig = MODE_OPTIONS.find((option) => option.key === analysisMode)!;

  useEffect(() => {
    if (!attachmentsAllowed) {
      setUploadedFile(null);
      setUploadedVoice(null);
    }
  }, [attachmentsAllowed]);

  const trimmedCurrentMessage = message.trim();
  const canSend = analysisMode === "predict"
    ? Boolean(trimmedCurrentMessage)
    : Boolean(trimmedCurrentMessage || uploadedFile || uploadedVoice);

  const handleSend = async () => {
    if (isLoading) return;

    const trimmedMessage = message.trim();

    if (analysisMode === "predict" && !trimmedMessage) {
      toast.error(t('common.enterQuestion'));
      return;
    }

    if (analysisMode !== "predict" && !trimmedMessage && !uploadedFile && !uploadedVoice) {
      toast.error(t('common.provideInput'));
      return;
    }

    const userContentParts: string[] = [];
    if (trimmedMessage) {
      userContentParts.push(trimmedMessage);
    }
    if (uploadedFile) {
      userContentParts.push(`[${t('common.document')}: ${uploadedFile.name}]`);
    }
    if (uploadedVoice) {
      userContentParts.push(`[${t('common.voice')}: ${uploadedVoice.name}]`);
    }

    const userDisplay = userContentParts.join("\n") || t('common.inputSubmitted');

    setMessages((prev) => [...prev, { role: "user", content: userDisplay }]);
    setMessage("");
    setIsLoading(true);

    try {
      let assistantContent = "";

      if (analysisMode === "predict") {
        const response = await apiService.predict(trimmedMessage, language);
        assistantContent = formatAssistantResponse(activeModeConfig.responseTitle, response.prediction, t, {
          input: response.input,
        });
      } else if (analysisMode === "analyze") {
        const response = await apiService.analyze({
          text: trimmedMessage || undefined,
          file: uploadedFile || undefined,
          voice: uploadedVoice || undefined,
          language: language,
        });
        assistantContent = formatAssistantResponse(activeModeConfig.responseTitle, response.prediction, t, {
          input: response.input_text,
          documentId: response.document_id,
        });
      } else {
        const response = await apiService.research({
          text: trimmedMessage || undefined,
          file: uploadedFile || undefined,
          voice: uploadedVoice || undefined,
          language: language,
        });
        assistantContent = formatAssistantResponse(activeModeConfig.responseTitle, response.prediction, t, {
          input: response.input_text,
          documentId: response.document_id,
        });
      }

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: assistantContent,
        },
      ]);

      toast.success(activeModeConfig.successMessage);
    } catch (error) {
      console.error("API Error:", error);
      const errorMessage =
        error instanceof Error ? error.message : t('common.unableToProcess');

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: `${t('common.requestFailed')}: ${errorMessage}`,
        },
      ]);

      toast.error(t('common.backendUnreachable'));
    } finally {
      setIsLoading(false);
      setUploadedFile(null);
      setUploadedVoice(null);
    }
  };

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setUploadedFile(file);
      toast.success(`${t('common.fileUploaded')} "${file.name}"`);
    }
  };

  const handleVoiceUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setUploadedVoice(file);
      toast.success(`${t('common.voiceFileUploaded')} "${file.name}"`);
    }
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      
      <main className="flex-1 pt-16">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-12">
          {/* Header */}
          <div className="max-w-4xl mx-auto mb-8 animate-fade-in">
            <div className="flex items-center gap-2 mb-4">
              <Sparkles className="w-5 h-5 text-primary" />
              <Badge variant="secondary" className="text-xs">{t('askAI.badge1')}</Badge>
              <Badge variant="outline" className="text-xs gap-1">
                <Shield className="w-3 h-3" />
                {t('askAI.badge2')}
              </Badge>
            </div>
            <h1 className="text-4xl font-bold mb-3">{t('askAI.title')}</h1>
            <p className="text-lg text-muted-foreground">
              {t('askAI.description')}
            </p>
          </div>

          {/* Chat Area */}
          <div className="max-w-4xl mx-auto">
            <Card className="gradient-card p-6 mb-6 min-h-[400px] flex flex-col animate-scale-in">
              <div className="flex flex-wrap gap-2 mb-6">
                {MODE_OPTIONS.map((option) => {
                  const isActive = option.key === analysisMode;
                  return (
                    <button
                      key={option.key}
                      type="button"
                      onClick={() => setAnalysisMode(option.key)}
                      disabled={isLoading}
                      className={`rounded-lg border px-4 py-3 text-left transition-smooth min-w-[160px] ${
                        isActive
                          ? "border-primary bg-primary/10 shadow-sm"
                          : "border-border hover:border-primary"
                      } ${isLoading ? "opacity-60" : ""}`}
                    >
                      <p className={`text-sm font-semibold ${isActive ? "text-primary" : ""}`}>
                        {option.label}
                      </p>
                      <p className="text-xs text-muted-foreground">{option.description}</p>
                    </button>
                  );
                })}
              </div>

              {messages.length === 0 ? (
                <div className="flex-1 flex flex-col items-center justify-center text-center">
                  <MessageSquare className="w-16 h-16 text-muted-foreground/30 mb-4" />
                  <h3 className="text-lg font-semibold mb-2">{t('askAI.startConversation')}</h3>
                  <p className="text-sm text-muted-foreground mb-6 max-w-md">
                    {t('askAI.startConversation.description')}
                  </p>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3 w-full max-w-2xl">
                    {suggestions.map((suggestion, idx) => (
                      <button
                        key={idx}
                        onClick={() => {
                          setAnalysisMode("predict");
                          setMessage(suggestion);
                        }}
                        className="text-left p-3 rounded-lg border border-border hover:border-primary hover:bg-primary/5 transition-smooth text-sm"
                      >
                        {suggestion}
                      </button>
                    ))}
                  </div>
                </div>
              ) : (
                <div className="flex-1 space-y-4 mb-4 overflow-y-auto">
                  {messages.map((msg, idx) => (
                    <div
                      key={idx}
                      className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
                    >
                      {msg.role === "user" ? (
                        <div className="max-w-[80%] p-4 rounded-2xl bg-primary text-primary-foreground">
                          <p className="text-sm leading-relaxed whitespace-pre-line">{msg.content}</p>
                        </div>
                      ) : (
                        <div className="max-w-[85%]">
                          <ResponseFormatter 
                            content={msg.content}
                          />
                        </div>
                      )}
                    </div>
                  ))}
                  {isLoading && (
                    <div className="flex justify-start">
                      <div className="max-w-[80%] p-4 rounded-2xl bg-muted">
                        <div className="flex gap-1">
                          <div className="w-2 h-2 rounded-full bg-muted-foreground animate-bounce" style={{ animationDelay: "0ms" }} />
                          <div className="w-2 h-2 rounded-full bg-muted-foreground animate-bounce" style={{ animationDelay: "150ms" }} />
                          <div className="w-2 h-2 rounded-full bg-muted-foreground animate-bounce" style={{ animationDelay: "300ms" }} />
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* File Upload Indicators */}
              {(uploadedFile || uploadedVoice) && (
                <div className="mb-4 p-3 bg-muted rounded-lg">
                  <p className="text-sm font-medium mb-2">{t('common.uploadedFiles')}:</p>
                  {uploadedFile && (
                    <div className="flex items-center gap-2 text-sm text-muted-foreground">
                      <Upload className="w-4 h-4" />
                      <span>{t('common.document')}: {uploadedFile.name}</span>
                      <button
                        onClick={() => setUploadedFile(null)}
                        className="text-destructive hover:underline"
                      >
                        {t('common.remove')}
                      </button>
                    </div>
                  )}
                  {uploadedVoice && (
                    <div className="flex items-center gap-2 text-sm text-muted-foreground mt-1">
                      <Mic className="w-4 h-4" />
                      <span>{t('common.voice')}: {uploadedVoice.name}</span>
                      <button
                        onClick={() => setUploadedVoice(null)}
                        className="text-destructive hover:underline"
                      >
                        {t('common.remove')}
                      </button>
                    </div>
                  )}
                </div>
              )}

              {/* Input Area */}
              <div className="flex gap-2">
                <div className="flex-1">
                  <Textarea
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    onKeyDown={(e) => {
                      if (e.key === "Enter" && !e.shiftKey) {
                        e.preventDefault();
                        handleSend();
                      }
                    }}
                    placeholder={MODE_PLACEHOLDER[analysisMode]}
                    className="min-h-[60px] resize-none"
                    disabled={isLoading}
                  />
                  {attachmentsAllowed ? (
                    <>
                      <div className="flex flex-wrap gap-2 mt-2">
                        <div className={`relative ${isLoading ? "opacity-60" : ""}`}>
                          <input
                            type="file"
                            accept=".pdf,.docx,.txt"
                            onChange={handleFileUpload}
                            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                            disabled={isLoading}
                          />
                          <Button
                            type="button"
                            variant="outline"
                            size="sm"
                            className="gap-2 pointer-events-none"
                            disabled={isLoading}
                          >
                            <Upload className="w-4 h-4" />
                            {t('askAI.uploadDocument')}
                          </Button>
                        </div>
                        <div className={`relative ${isLoading ? "opacity-60" : ""}`}>
                          <input
                            type="file"
                            accept=".wav,.mp3,.m4a,.ogg"
                            onChange={handleVoiceUpload}
                            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                            disabled={isLoading}
                          />
                          <Button
                            type="button"
                            variant="outline"
                            size="sm"
                            className="gap-2 pointer-events-none"
                            disabled={isLoading}
                          >
                            <Mic className="w-4 h-4" />
                            {t('askAI.uploadVoice')}
                          </Button>
                        </div>
                      </div>
                      <p className="mt-2 text-xs text-muted-foreground">
                        {t('askAI.fileFormats')}
                      </p>
                    </>
                  ) : (
                    <p className="mt-2 text-xs text-muted-foreground">
                      {t('askAI.textOnlyMode')}
                    </p>
                  )}
                </div>
                <Button
                  onClick={handleSend}
                  disabled={!canSend || isLoading}
                  size="icon"
                  className="h-[60px] w-[60px] shrink-0"
                >
                  <Send className="w-5 h-5" />
                </Button>
              </div>
            </Card>

            {/* Privacy Notice */}
            <div className="flex items-start gap-3 p-4 rounded-lg bg-success/5 border border-success/20">
              <Shield className="w-5 h-5 text-success shrink-0 mt-0.5" />
              <div>
                <h4 className="text-sm font-semibold mb-1">{t('askAI.privacyNotice.title')}</h4>
                <p className="text-xs text-muted-foreground">
                  {t('askAI.privacyNotice.description')}
                </p>
              </div>
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default AskAI;
