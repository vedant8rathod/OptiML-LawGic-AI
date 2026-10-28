import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Checkbox } from "@/components/ui/checkbox";
import { ShieldAlert, Download, Copy, Check } from "lucide-react";
import { toast } from "sonner";
import { apiService } from "@/services/api";

interface PrivacyRedactionPanelProps {
  originalText: string;
}

const PrivacyRedactionPanel: React.FC<PrivacyRedactionPanelProps> = ({ originalText }) => {
  const [selectedCategories, setSelectedCategories] = useState<string[]>([
    "PERSON",
    "PHONE",
    "EMAIL",
    "MONEY",
  ]);
  const [redactedText, setRedactedText] = useState<string>("");
  const [redactedCount, setRedactedCount] = useState<number>(0);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [copied, setCopied] = useState<boolean>(false);

  const categories = [
    { id: "PERSON", label: "Person Names" },
    { id: "PHONE", label: "Phone Numbers" },
    { id: "EMAIL", label: "Email Addresses" },
    { id: "MONEY", label: "Financial Amounts" },
    { id: "ORGANIZATION", label: "Organizations" },
  ];

  const handleToggle = (catId: string) => {
    setSelectedCategories((prev) =>
      prev.includes(catId) ? prev.filter((c) => c !== catId) : [...prev, catId]
    );
  };

  const handleRedact = async () => {
    if (!originalText) return;
    setIsLoading(true);
    try {
      const res = await apiService.redactEntities(originalText, selectedCategories);
      setRedactedText(res.redacted_text);
      setRedactedCount(res.redacted_count);
      toast.success(`Redacted ${res.redacted_count} sensitive entity occurrences.`);
    } catch (err: any) {
      toast.error(err.message || "Redaction failed.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleCopy = () => {
    if (!redactedText) return;
    navigator.clipboard.writeText(redactedText);
    setCopied(true);
    toast.success("Redacted text copied to clipboard.");
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    if (!redactedText) return;
    const blob = new Blob([redactedText], { type: "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "redacted_document.txt";
    link.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-4 border border-border/70 rounded-xl p-4 bg-card shadow-sm">
      <div className="flex items-center gap-2">
        <ShieldAlert className="w-5 h-5 text-primary" />
        <div>
          <h3 className="text-sm font-semibold">Privacy-Preserving PII Redaction</h3>
          <p className="text-xs text-muted-foreground">
            Select entity categories to sanitize before sharing or filing documents.
          </p>
        </div>
      </div>

      <div className="flex flex-wrap gap-4 pt-1">
        {categories.map((c) => (
          <label key={c.id} className="flex items-center gap-2 text-xs font-medium cursor-pointer">
            <Checkbox
              checked={selectedCategories.includes(c.id)}
              onCheckedChange={() => handleToggle(c.id)}
            />
            {c.label}
          </label>
        ))}
      </div>

      <div className="flex gap-2">
        <Button
          size="sm"
          onClick={handleRedact}
          disabled={isLoading || !originalText || selectedCategories.length === 0}
          className="gap-2"
        >
          {isLoading ? "Sanitizing..." : "Execute Redaction"}
        </Button>
      </div>

      {redactedText && (
        <div className="space-y-2 pt-2 border-t border-border/50">
          <div className="flex items-center justify-between">
            <Badge variant="outline" className="text-xs gap-1 border-emerald-300 text-emerald-700 bg-emerald-50">
              {redactedCount} entities sanitized
            </Badge>
            <div className="flex gap-2">
              <Button size="sm" variant="outline" onClick={handleCopy} className="h-7 text-xs gap-1">
                {copied ? <Check className="w-3 h-3 text-emerald-600" /> : <Copy className="w-3 h-3" />}
                Copy
              </Button>
              <Button size="sm" variant="outline" onClick={handleDownload} className="h-7 text-xs gap-1">
                <Download className="w-3 h-3" />
                Download
              </Button>
            </div>
          </div>

          <div className="bg-muted/50 border border-border/60 rounded-lg p-3 text-xs font-mono max-h-48 overflow-y-auto whitespace-pre-wrap leading-relaxed">
            {redactedText}
          </div>
        </div>
      )}
    </div>
  );
};

export default PrivacyRedactionPanel;
