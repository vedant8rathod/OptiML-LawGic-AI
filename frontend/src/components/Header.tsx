import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Scale, Menu, Globe } from "lucide-react";
import { useLanguage } from "@/contexts/LanguageContext";

const Header = () => {
  const { language, setLanguage, t } = useLanguage();
  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-background/80 backdrop-blur-md border-b border-border">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="flex items-center gap-2 group">
            <img
              src="/Lawgic_logo.png"
              alt="LawGic Logo"
              className="w-8 h-8 object-contain rounded group-hover:scale-110 transition-smooth"
              loading="eager"
              decoding="async"
              onError={(e) => { (e.currentTarget as HTMLImageElement).src = '/placeholder.svg'; }}
            />
            <span className="font-semibold text-lg tracking-tight text-black">
              {t('brand.name')}
            </span>
          </Link>

          <nav className="hidden md:flex items-center gap-6">
            <Link
              to="/ask-ai"
              className="text-sm font-medium text-muted-foreground hover:text-foreground transition-smooth"
            >
              {t('header.askAI')}
            </Link>
            <Link
              to="/entities"
              className="text-sm font-medium text-muted-foreground hover:text-foreground transition-smooth"
            >
              Legal Entities
            </Link>
            <Link
              to="/#features"
              className="text-sm font-medium text-muted-foreground hover:text-foreground transition-smooth"
            >
              {t('header.features')}
            </Link>
            <Link
              to="/#how-it-works"
              className="text-sm font-medium text-muted-foreground hover:text-foreground transition-smooth"
            >
              {t('header.howItWorks')}
            </Link>
            <Link
              to="/#trust"
              className="text-sm font-medium text-muted-foreground hover:text-foreground transition-smooth"
            >
              {t('header.privacy')}
            </Link>
          </nav>

          <div className="flex items-center gap-3">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setLanguage(language === 'en' ? 'hi' : 'en')}
              className="hidden md:inline-flex gap-2"
            >
              <Globe className="w-4 h-4" />
              {language === 'en' ? 'हिं' : 'EN'}
            </Button>
            <Button asChild variant="ghost" className="hidden md:inline-flex">
              <Link to="/ask-ai">{t('header.getStarted')}</Link>
            </Button>
            <Button asChild size="sm" className="hidden md:inline-flex">
              <Link to="/ask-ai">{t('header.askLegalAI')}</Link>
            </Button>
            <Button variant="ghost" size="icon" className="md:hidden">
              <Menu className="w-5 h-5" />
            </Button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
