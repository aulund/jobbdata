"""
Database module for storing and retrieving genetic variant data.
Uses SQLite with SQLAlchemy ORM for persistence.
"""

import os
import logging
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import config

logger = logging.getLogger(__name__)

Base = declarative_base()


class VariantRecord(Base):
    """Database model for storing variant records."""
    __tablename__ = 'variants'
    
    id = Column(Integer, primary_key=True)
    lid_nr = Column(String(100), nullable=False, index=True)
    gene = Column(String(50), nullable=False, index=True)
    nucleotide_change = Column(String(200))
    protein_change = Column(String(200))
    zygosity = Column(String(50))
    inheritance = Column(String(100))
    acmg_assessment = Column(String(100))
    clinvar_info = Column(Text)
    further_studies = Column(String(10))
    transcript = Column(String(50))
    disease = Column(String(200))
    category = Column(String(50))
    
    # Patient information
    proband = Column(String(200))
    genotype = Column(String(200))
    phenotype = Column(String(200))
    sequencing_method = Column(String(50))
    exon = Column(String(50))
    
    # Metadata
    is_normal_finding = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    
    def __repr__(self):
        return f"<VariantRecord(lid_nr='{self.lid_nr}', gene='{self.gene}')>"


class VariantDatabase:
    """Manager class for database operations."""
    
    def __init__(self, db_path=None):
        """
        Initialize database connection.
        
        Args:
            db_path: Path to SQLite database file. Defaults to 'variants.db' in current directory.
        """
        if db_path is None:
            db_path = os.path.join(os.getcwd(), 'variants.db')
        
        self.db_path = db_path
        self.engine = create_engine(f'sqlite:///{db_path}', echo=False)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        logger.info(f"Database initialized at {db_path}")
    
    def save_variant_data(self, data):
        """
        Save variant data to database.
        
        Args:
            data: Dictionary containing variant and patient information
            
        Returns:
            list: List of saved record IDs
        """
        try:
            saved_ids = []
            
            # Check if this is a normal finding
            if data.get("Normalfynd", False):
                record = VariantRecord(
                    lid_nr=data.get("LID-NR", ""),
                    gene=data.get("Gene", ""),
                    transcript=data.get("Transcript", ""),
                    disease=data.get("Disease", ""),
                    category=data.get("Category", ""),
                    proband=data.get("Proband", ""),
                    genotype=data.get("Genotype", ""),
                    phenotype=data.get("Phenotype", ""),
                    sequencing_method=data.get("Sequencing method", ""),
                    exon=data.get("Exon", ""),
                    is_normal_finding=True
                )
                self.session.add(record)
                self.session.commit()
                saved_ids.append(record.id)
                logger.info(f"Saved normal finding record with ID {record.id}")
            else:
                # Save each variant
                for variant in data.get("variants", []):
                    record = VariantRecord(
                        lid_nr=data.get("LID-NR", ""),
                        gene=variant.get("Gene", ""),
                        nucleotide_change=variant.get("Nucleotide change", ""),
                        protein_change=variant.get("Protein change", ""),
                        zygosity=variant.get("Zygosity", ""),
                        inheritance=variant.get("Inheritance", ""),
                        acmg_assessment=variant.get("ACMG criteria assessment", ""),
                        clinvar_info=variant.get("ClinVar and hemophilia database reports", ""),
                        further_studies=variant.get("Further studies", ""),
                        transcript=data.get("Transcript", ""),
                        disease=data.get("Disease", ""),
                        category=data.get("Category", ""),
                        proband=data.get("Proband", ""),
                        genotype=data.get("Genotype", ""),
                        phenotype=data.get("Phenotype", ""),
                        sequencing_method=data.get("Sequencing method", ""),
                        exon=data.get("Exon", ""),
                        is_normal_finding=False
                    )
                    self.session.add(record)
                    self.session.commit()
                    saved_ids.append(record.id)
                    logger.info(f"Saved variant record with ID {record.id}")
            
            return saved_ids
            
        except Exception as e:
            logger.error(f"Error saving variant data: {e}", exc_info=True)
            self.session.rollback()
            return []
    
    def get_variants_by_lid(self, lid_nr):
        """
        Retrieve all variants for a specific LID-NR.
        
        Args:
            lid_nr: The LID-NR to search for
            
        Returns:
            list: List of VariantRecord objects
        """
        try:
            records = self.session.query(VariantRecord).filter_by(lid_nr=lid_nr).all()
            logger.info(f"Retrieved {len(records)} records for LID-NR {lid_nr}")
            return records
        except Exception as e:
            logger.error(f"Error retrieving variants: {e}", exc_info=True)
            return []
    
    def get_variants_by_gene(self, gene):
        """
        Retrieve all variants for a specific gene.
        
        Args:
            gene: The gene name to search for
            
        Returns:
            list: List of VariantRecord objects
        """
        try:
            records = self.session.query(VariantRecord).filter_by(gene=gene).all()
            logger.info(f"Retrieved {len(records)} records for gene {gene}")
            return records
        except Exception as e:
            logger.error(f"Error retrieving variants: {e}", exc_info=True)
            return []
    
    def get_all_variants(self, limit=100):
        """
        Retrieve all variant records.
        
        Args:
            limit: Maximum number of records to retrieve
            
        Returns:
            list: List of VariantRecord objects
        """
        try:
            records = self.session.query(VariantRecord).order_by(
                VariantRecord.created_at.desc()
            ).limit(limit).all()
            logger.info(f"Retrieved {len(records)} total records")
            return records
        except Exception as e:
            logger.error(f"Error retrieving all variants: {e}", exc_info=True)
            return []
    
    def close(self):
        """Close the database session."""
        self.session.close()
        logger.info("Database session closed")
