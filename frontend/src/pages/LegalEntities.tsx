import React, { useState } from "react";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Textarea } from "@/components/ui/textarea";
import {
  FileText,
  Upload,
  Sparkles,
  Download,
  Shield,
  Layers,
  Network,
  Calendar,
  Eye,
  RefreshCw,
} from "lucide-react";
import { toast } from "sonner";
import { apiService } from "@/services/api";
import SmartEntityHighlighter, { EntityItem } from "@/components/entities/SmartEntityHighlighter";
import LegalEntityExplorer from "@/components/entities/LegalEntityExplorer";
import EntityDetailPanel from "@/components/entities/EntityDetailPanel";
import LegalRelationTable, { LegalRelationItem } from "@/components/entities/LegalRelationTable";
import LegalTimeline, { TimelineEventItem } from "@/components/entities/LegalTimeline";
import PrivacyRedactionPanel from "@/components/entities/PrivacyRedactionPanel";

const SAMPLE_LEGAL_DOC = `IN THE SUPREME COURT OF INDIA
CIVIL APPELLATE JURISDICTION
Writ Petition (Civil) No. 402 of 2021

In the matter of:
ABC Technologies Pvt. Ltd., New Delhi
... Petitioner

Versus

Mr. Rajesh Sharma & Ors.
... Respondents

Coram:
Hon'ble Chief Justice D.Y. Chandrachud

For the Petitioner: Mr. Harish Salve, Senior Advocate
For the Respondent: Adv. Amit Sibal

ORDER / JUDGMENT:
The Petitioner, ABC Technologies Pvt. Ltd., filed the present petition on 15/08/2021 seeking enforcement of agreement clauses and claim for damages of ₹5,00,000 against Respondent Mr. Rajesh Sharma.
The petition invokes Section 138 of the Negotiable Instruments Act read with Section 420 of the Indian Penal Code, 1860.
The parties entered into an agreement dated 10/01/2020 at Mumbai. The Respondent issued a cheque for INR 5,00,000 on 05/03/2021, which was dishonored.
For all procedural notices, the registry shall direct correspondence to legal@abctech.com or telephone +91 98765 43210.
Decided on 20/09/2021.`;

const LegalEntities = () => {
  const [inputText, setInputText] = useState(SAMPLE_LEGAL_DOC);
  const [activeTab, setActiveTab] = useState("highlighter");
  const [isLoading, setIsLoading] = useState(false);
  const [analysisData, setAnalysisData] = useState<any>(null);
  const [selectedEntity, setSelectedEntity] = useState<EntityItem | null>(null);
  const [filterCategory, setFilterCategory] = useState<string>("ALL");

  const runAnalysis = async (textToAnalyze: string) => {
    if (!textToAnalyze.trim()) {
      toast.error("Please provide text or upload a document.");
      return;
    }
    setIsLoading(true);
    setSelectedEntity(null);

    try {
      const data = await apiService.analyzeEntitiesText(textToAnalyze);
      setAnalysisData(data);
      toast.success(`Successfully analyzed ${data.stats.total_entities} entities and ${data.stats.total_relations} relationships.`);
    } catch (err: any) {
      toast.error(err.message || "Failed to analyze document.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setIsLoading(true);
    setSelectedEntity(null);
    try {
      const data = await apiService.analyzeEntitiesFile(file);
      setAnalysisData(data);
      setInputText(data.text || "");
      toast.success(`Processed "${file.name}": ${data.stats.total_entities} entities found.`);
    } catch (err: any) {
      toast.error(err.message || "File processing failed.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleSelectEntity = (ent: EntityItem) => {
    setSelectedEntity(ent);
  };

  // Find occurrences of the selected entity
  const currentOccurrences = React.useMemo(() => {
    if (!selectedEntity || !analysisData?.entities) return [];
    return analysisData.entities.filter(
      (e: EntityItem) =>
        e.text.toLowerCase().trim() === selectedEntity.text.toLowerCase().trim()
    );
  }, [selectedEntity, analysisData]);

  return (
    <div className="min-h-screen flex flex-col">
      <Header />

      <main className="flex-1 pt-20 pb-16">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 max-w-7xl">
          {/* Header */}
          <div className="mb-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <div className="flex items-center gap-2 mb-2">
                <Sparkles className="w-5 h-5 text-primary" />
                <Badge variant="secondary" className="text-xs">
                  Legal Entity Intelligence
                </Badge>
                <Badge variant="outline" className="text-xs gap-1 border-primary/40 text-primary">
                  <Shield className="w-3 h-3" />
                  NLP-Powered
                </Badge>
              </div>
              <h1 className="text-3xl font-bold tracking-tight">Legal Entity Intelligence & Explorer</h1>
              <p className="text-sm text-muted-foreground mt-1 max-w-2xl">
                Extract Indian statutes, court citations, monetary claims, case milestones, relationships, and sanitize sensitive data with privacy redaction.
              </p>
            </div>

            <div className="flex items-center gap-2">
              <label className="cursor-pointer">
                <input
                  type="file"
                  accept=".pdf,.docx,.txt"
                  onChange={handleFileUpload}
                  className="hidden"
                />
                <Button variant="outline" size="sm" className="gap-2 pointer-events-none" disabled={isLoading}>
                  <Upload className="w-4 h-4" />
                  Upload Legal Doc
                </Button>
              </label>

              {analysisData?.text && (
                <Button
                  variant="outline"
                  size="sm"
                  asChild
                  className="gap-2"
                >
                  <a
                    href={apiService.getEntitiesExportCsvUrl(analysisData.text)}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    <Download className="w-4 h-4" />
                    Export CSV
                  </a>
                </Button>
              )}

              <Button
                size="sm"
                onClick={() => runAnalysis(inputText)}
                disabled={isLoading}
                className="gap-2"
              >
                {isLoading ? (
                  <RefreshCw className="w-4 h-4 animate-spin" />
                ) : (
                  <Sparkles className="w-4 h-4" />
                )}
                Analyze Document
              </Button>
            </div>
          </div>

          {/* Quick Input Accordion / View */}
          {!analysisData && (
            <div className="mb-6 p-4 rounded-xl border border-border/80 bg-card shadow-sm space-y-3">
              <div className="flex items-center justify-between">
                <label className="text-xs font-semibold text-muted-foreground uppercase">
                  Document Input (or try with our sample Indian court judgment below)
                </label>
                <Button
                  variant="ghost"
                  size="sm"
                  className="text-xs h-6 px-2 text-primary"
                  onClick={() => setInputText(SAMPLE_LEGAL_DOC)}
                >
                  Reset Sample
                </Button>
              </div>
              <Textarea
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                rows={6}
                className="font-mono text-xs leading-relaxed"
                placeholder="Paste legal notice, petition, contract, or judgment text..."
              />
            </div>
          )}

          {/* Analysis Workspace */}
          {analysisData && (
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
              {/* Left / Main Column (7 cols) */}
              <div className="lg:col-span-8 space-y-4">
                <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
                  <div className="flex items-center justify-between pb-2 border-b border-border">
                    <TabsList className="bg-muted/60 p-1">
                      <TabsTrigger value="highlighter" className="text-xs gap-1.5">
                        <Eye className="w-3.5 h-3.5" />
                        Annotated Spans
                      </TabsTrigger>
                      <TabsTrigger value="relations" className="text-xs gap-1.5">
                        <Network className="w-3.5 h-3.5" />
                        Relationships ({analysisData.relations?.length || 0})
                      </TabsTrigger>
                      <TabsTrigger value="timeline" className="text-xs gap-1.5">
                        <Calendar className="w-3.5 h-3.5" />
                        Timeline ({analysisData.timeline?.length || 0})
                      </TabsTrigger>
                      <TabsTrigger value="redact" className="text-xs gap-1.5">
                        <Shield className="w-3.5 h-3.5" />
                        Privacy & Redact
                      </TabsTrigger>
                    </TabsList>

                    {activeTab === "highlighter" && (
                      <div className="flex items-center gap-2">
                        <span className="text-xs text-muted-foreground hidden sm:inline">Filter:</span>
                        <select
                          value={filterCategory}
                          onChange={(e) => setFilterCategory(e.target.value)}
                          className="text-xs bg-card border border-border rounded-md px-2 py-1"
                        >
                          <option value="ALL">All Categories</option>
                          <option value="STATUTE">Statutes</option>
                          <option value="LEGAL_PROVISION">Legal Provisions</option>
                          <option value="COURT">Courts</option>
                          <option value="CASE_NUMBER">Case Numbers</option>
                          <option value="MONEY">Financials</option>
                          <option value="DATE">Dates</option>
                          <option value="PERSON">Persons</option>
                          <option value="ORGANIZATION">Organizations</option>
                          <option value="ADVOCATE">Advocates</option>
                        </select>
                      </div>
                    )}
                  </div>

                  <TabsContent value="highlighter" className="pt-3">
                    <SmartEntityHighlighter
                      text={analysisData.text}
                      entities={analysisData.entities || []}
                      selectedEntity={selectedEntity}
                      onSelectEntity={handleSelectEntity}
                      filterCategory={filterCategory}
                    />
                  </TabsContent>

                  <TabsContent value="relations" className="pt-3">
                    <LegalRelationTable relations={analysisData.relations || []} />
                  </TabsContent>

                  <TabsContent value="timeline" className="pt-3">
                    <LegalTimeline timeline={analysisData.timeline || []} />
                  </TabsContent>

                  <TabsContent value="redact" className="pt-3">
                    <PrivacyRedactionPanel originalText={analysisData.text} />
                  </TabsContent>
                </Tabs>
              </div>

              {/* Right Sidebar (4 cols): Explorer & Detail */}
              <div className="lg:col-span-4 space-y-4">
                {/* Stats Widget */}
                <div className="grid grid-cols-2 gap-2">
                  <div className="p-3 rounded-xl border border-border/70 bg-card text-center">
                    <p className="text-[10px] uppercase font-semibold text-muted-foreground">Total Entities</p>
                    <p className="text-xl font-bold text-primary">{analysisData.stats.total_entities}</p>
                  </div>
                  <div className="p-3 rounded-xl border border-border/70 bg-card text-center">
                    <p className="text-[10px] uppercase font-semibold text-muted-foreground">Unique Mentions</p>
                    <p className="text-xl font-bold text-accent">{analysisData.stats.unique_entities}</p>
                  </div>
                </div>

                {/* Entity Details Popup if selected */}
                {selectedEntity && (
                  <EntityDetailPanel
                    entity={selectedEntity}
                    allOccurrences={currentOccurrences}
                    onClose={() => setSelectedEntity(null)}
                    onJumpToOccurrence={(start, end) => {
                      toast.info(`Highlighted entity span at character offset [${start}:${end}]`);
                    }}
                  />
                )}

                {/* Structured Explorer */}
                <div className="space-y-2">
                  <h3 className="text-xs font-bold uppercase text-muted-foreground tracking-wider flex items-center gap-1.5">
                    <Layers className="w-3.5 h-3.5 text-primary" />
                    Structured Entity Explorer
                  </h3>
                  <LegalEntityExplorer
                    groupedEntities={analysisData.grouped_entities || {}}
                    selectedEntity={selectedEntity}
                    onSelectEntity={handleSelectEntity}
                  />
                </div>
              </div>
            </div>
          )}
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default LegalEntities;
