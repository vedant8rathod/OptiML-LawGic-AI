import { Link } from "react-router-dom";
import { Scale, Heart } from "lucide-react";
import { useLanguage } from "@/contexts/LanguageContext";

const Footer = () => {
  const { t } = useLanguage();
  return (
    <footer className="border-t border-border bg-muted/30">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center gap-2 mb-4">
              <div className="w-8 h-8 rounded-lg bg-gradient-hero flex items-center justify-center shadow-glow">
                <Scale className="w-5 h-5 text-white" />
              </div>
              <span className="font-semibold text-lg">{t('brand.name')}</span>
            </div>
            <p className="text-sm text-muted-foreground mb-4 max-w-md">
              {t('hero.description')}
            </p>
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <span>{t('footer.madeWith')}</span>
              <Heart className="w-4 h-4 text-accent fill-accent" />
              <span>{t('footer.forJustice')}</span>
            </div>
          </div>

          <div>
            <h3 className="font-semibold mb-4">{t('features.title')}</h3>
            <ul className="space-y-2">
              <li>
                <Link to="/ask-ai" className="text-sm text-muted-foreground hover:text-foreground transition-smooth">
                  {t('header.askLegalAI')}
                </Link>
              </li>
              <li>
                <Link to="/#features" className="text-sm text-muted-foreground hover:text-foreground transition-smooth">
                  {t('header.features')}
                </Link>
              </li>
              <li>
                <Link to="/#how-it-works" className="text-sm text-muted-foreground hover:text-foreground transition-smooth">
                  {t('header.howItWorks')}
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h3 className="font-semibold mb-4">{t('footer.about')}</h3>
            <ul className="space-y-2">
              <li>
                <Link to="/privacy" className="text-sm text-muted-foreground hover:text-foreground transition-smooth">
                  {t('footer.privacyPolicy')}
                </Link>
              </li>
              <li>
                <Link to="/terms" className="text-sm text-muted-foreground hover:text-foreground transition-smooth">
                  {t('footer.termsOfService')}
                </Link>
              </li>
              <li>
                <Link to="/#trust" className="text-sm text-muted-foreground hover:text-foreground transition-smooth">
                  {t('header.privacy')}
                </Link>
              </li>
            </ul>
          </div>
        </div>

        <div className="mt-8 pt-8 border-t border-border">
          <p className="text-sm text-muted-foreground text-center">
            {t('footer.copyright').replace('2024', new Date().getFullYear().toString())}
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
